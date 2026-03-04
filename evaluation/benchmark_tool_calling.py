import argparse
import ast
import csv
import json
import os
import py_compile
import random
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Any, Dict, List, Tuple

from build_benchmark_prompt import build_prompt


ROOT = Path(__file__).resolve().parents[1]
CSV_PATH_DEFAULT = ROOT / "datasets" / "test_data.csv"
CATALOG_PATH = ROOT / "tools" / "api_catalog.json"


def _load_invoke():
    import importlib.util

    adapter_path = ROOT / "tools" / "llm_api_adapter.py"
    spec = importlib.util.spec_from_file_location("llm_api_adapter_runtime", adapter_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.invoke


INVOKE = _load_invoke()


def to_float(value: Any):
    try:
        return float(value)
    except Exception:
        return None


def normalize_non_numeric(value: Any):
    if isinstance(value, tuple):
        return tuple(str(x).strip().lower() for x in value)
    if isinstance(value, list):
        return [str(x).strip().lower() for x in value]
    # Cast whole-number floats to int before stringifying so 112.0 matches "112"
    if isinstance(value, float) and value.is_integer():
        return str(int(value))
    return str(value).strip().lower()


def parse_json_loose(text: str):
    text = (text or "").strip()
    if not text:
        raise ValueError("empty model response")

    # Try direct JSON parse first.
    try:
        return json.loads(text)
    except Exception:
        pass

    # Strip markdown fence if present.
    if "```" in text:
        chunks = text.split("```")
        for chunk in chunks:
            cleaned = chunk.strip()
            if cleaned.startswith("json"):
                cleaned = cleaned[4:].strip()
            if cleaned.startswith("{") and cleaned.endswith("}"):
                try:
                    return json.loads(cleaned)
                except Exception:
                    pass

    # Fallback: first JSON object in string.
    start = text.find("{")
    end = text.rfind("}")
    if start >= 0 and end > start:
        maybe = text[start : end + 1]
        return json.loads(maybe)

    raise ValueError("response does not contain valid JSON object")


def score_prediction(
    prediction: Any, gt_raw: str, tolerance: float, force_string_match: bool = False,
    force_float_string_match: bool = False,
) -> Tuple[bool, Dict[str, Any]]:
    if force_float_string_match:
        try:
            pred_str = str(float(prediction))
            gt_str = str(float(gt_raw))
            passed = pred_str == gt_str
        except Exception:
            passed = str(prediction).strip() == str(gt_raw).strip()
            pred_str, gt_str = str(prediction), str(gt_raw)
        return passed, {"mode": "float_string", "pred": pred_str, "gt": gt_str}

    if force_string_match:
        gt_value = gt_raw
        try:
            gt_value = ast.literal_eval(gt_raw)
        except Exception:
            pass
        passed = normalize_non_numeric(prediction) == normalize_non_numeric(gt_value)
        return passed, {
            "mode": "forced_string",
            "pred": prediction,
            "gt": gt_value,
        }

    gt_num = to_float(gt_raw)
    pred_num = to_float(prediction)

    if gt_num is not None and pred_num is not None:
        if gt_num == 0:
            passed = abs(pred_num - gt_num) <= tolerance
        else:
            rel_err = abs(pred_num - gt_num) / abs(gt_num)
            passed = rel_err <= tolerance
        return passed, {"mode": "numeric", "pred_num": pred_num, "gt_num": gt_num}

    gt_value = gt_raw
    try:
        gt_value = ast.literal_eval(gt_raw)
    except Exception:
        pass
    passed = normalize_non_numeric(prediction) == normalize_non_numeric(gt_value)
    return passed, {"mode": "non_numeric", "pred": prediction, "gt": gt_value}


def should_force_string_match(calc_id: int, category: str) -> bool:
    if calc_id in {13, 68, 69}:
        return True
    return (category or "").strip().lower() in {"date"}


def should_force_float_string_match(calc_id: int) -> bool:
    # Convert both prediction and GT to float then compare as strings
    return calc_id in {8}


class OpenAIClient:
    def __init__(self):
        from openai import OpenAI

        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    def run(self, model: str, prompt: str) -> str:
        resp = self.client.chat.completions.create(
            model=model,
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": "You are a strict JSON tool-calling assistant."},
                {"role": "user", "content": prompt},
            ],
        )
        return resp.choices[0].message.content or ""


class AnthropicClient:
    def __init__(self):
        import anthropic

        self.client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

    def run(self, model: str, prompt: str) -> str:
        resp = self.client.messages.create(
            model=model,
            max_tokens=1024,
            system="You are a strict JSON tool-calling assistant. Output valid JSON only.",
            messages=[{"role": "user", "content": prompt}],
        )
        return resp.content[0].text if resp.content else ""


class GeminiClient:
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("Set GEMINI_API_KEY or GOOGLE_API_KEY")

        self.backend = None
        self.client = None
        self.genai = None

        # Preferred new SDK path.
        try:
            from google import genai

            self.genai = genai
            self.client = genai.Client(api_key=api_key)
            self.backend = "google.genai"
            return
        except Exception:
            pass

        # Fallback old SDK.
        import google.generativeai as genai_legacy

        genai_legacy.configure(api_key=api_key)
        self.client = genai_legacy
        self.backend = "google.generativeai"

    def run(self, model: str, prompt: str) -> str:
        if self.backend == "google.genai":
            resp = self.client.models.generate_content(
                model=model,
                contents=prompt,
                config=self.genai.types.GenerateContentConfig(
                    temperature=0,
                    response_mime_type="application/json",
                ),
            )
            return getattr(resp, "text", "") or ""

        # Legacy backend.
        m = self.client.GenerativeModel(model)
        resp = m.generate_content(
            prompt,
            generation_config={"temperature": 0, "response_mime_type": "application/json"},
        )
        return getattr(resp, "text", "") or ""


def load_rows(csv_path: Path) -> List[Dict[str, str]]:
    with csv_path.open(newline="") as f:
        return list(csv.DictReader(f))


def run_compile_preflight():
    """Abort immediately if benchmark dependencies have compile errors."""
    to_compile = [
        ROOT / "evaluation" / "build_benchmark_prompt.py",
        ROOT / "tools" / "llm_api_adapter.py",
    ]

    catalog = json.loads(CATALOG_PATH.read_text())
    for entry in catalog:
        tool_module = entry.get("tool_module")
        if tool_module:
            to_compile.append(ROOT / "tools" / tool_module)

    errors = []
    seen = set()
    for path in to_compile:
        if path in seen:
            continue
        seen.add(path)
        try:
            py_compile.compile(str(path), doraise=True)
        except Exception as exc:
            errors.append(f"{path}: {exc}")

    if errors:
        formatted = "\n".join(errors)
        raise RuntimeError(f"Compile preflight failed. Aborting run.\n{formatted}")


def sample_rows_per_calculator(
    rows: List[Dict[str, str]], samples_per_calculator: int, seed: int
) -> List[Dict[str, str]]:
    grouped: Dict[str, List[Dict[str, str]]] = {}
    for r in rows:
        calc_id = str(r["Calculator ID"]).strip()
        grouped.setdefault(calc_id, []).append(r)

    rnd = random.Random(seed)
    sampled = []
    for calc_id in sorted(grouped, key=lambda x: int(x)):
        items = grouped[calc_id]
        k = min(samples_per_calculator, len(items))
        sampled.extend(rnd.sample(items, k))
    return sampled


def run_one(
    row: Dict[str, str],
    provider: str,
    model: str,
    client: Any,
    tolerance: float,
):
    calc_id = int(row["Calculator ID"])
    row_number = row.get("Row Number")
    calc_name = row.get("Calculator Name")
    category = row.get("Category", "")
    task_input = json.dumps(
        {
            "patient_note": row.get("Patient Note", ""),
            "question": row.get("Question", ""),
            "relevant_entities": row.get("Relevant Entities", ""),
        },
        ensure_ascii=False,
        indent=2,
    )

    prompt = build_prompt(calc_id, task_input)
    raw_response = client.run(model, prompt)

    try:
        parsed = parse_json_loose(raw_response)
    except Exception as exc:
        return {
            "status": "tool_error",
            "provider": provider,
            "model": model,
            "row_number": row_number,
            "calculator_id": calc_id,
            "calculator_name": calc_name,
            "ground_truth": row.get("Ground Truth Answer"),
            "raw_model_response": raw_response,
            "parsed_model_json": None,
            "invoke_out": {"ok": False, "errors": {"response": str(exc)}},
            "correct": False,
        }

    if "calculator_id" not in parsed or "arguments" not in parsed:
        return {
            "status": "tool_error",
            "provider": provider,
            "model": model,
            "row_number": row_number,
            "calculator_id": calc_id,
            "calculator_name": calc_name,
            "ground_truth": row.get("Ground Truth Answer"),
            "raw_model_response": raw_response,
            "parsed_model_json": parsed,
            "invoke_out": {
                "ok": False,
                "errors": {"response": "model JSON must contain calculator_id and arguments"},
            },
            "correct": False,
        }

    invoke_out = INVOKE(str(parsed["calculator_id"]), parsed["arguments"])
    if not invoke_out.get("ok"):
        return {
            "status": "tool_error",
            "provider": provider,
            "model": model,
            "row_number": row_number,
            "calculator_id": calc_id,
            "calculator_name": calc_name,
            "ground_truth": row.get("Ground Truth Answer"),
            "raw_model_response": raw_response,
            "parsed_model_json": parsed,
            "invoke_out": invoke_out,
            "correct": False,
        }

    prediction = invoke_out.get("result")
    force_string = should_force_string_match(calc_id, category)
    force_float_string = should_force_float_string_match(calc_id)
    correct, detail = score_prediction(
        prediction,
        row.get("Ground Truth Answer", ""),
        tolerance,
        force_string_match=force_string,
        force_float_string_match=force_float_string,
    )
    return {
        "status": "ok",
        "provider": provider,
        "model": model,
        "row_number": row_number,
        "calculator_id": calc_id,
        "calculator_name": calc_name,
        "ground_truth": row.get("Ground Truth Answer"),
        "prediction": prediction,
        "score_detail": detail,
        "raw_model_response": raw_response,
        "parsed_model_json": parsed,
        "invoke_out": invoke_out,
        "correct": bool(correct),
    }


def summarize(results: List[Dict[str, Any]]):
    by_model: Dict[str, Dict[str, int]] = {}
    for r in results:
        key = f"{r['provider']}::{r['model']}"
        s = by_model.setdefault(
            key,
            {"total": 0, "ok": 0, "correct": 0, "tool_error": 0, "exception": 0},
        )
        s["total"] += 1
        if r["status"] == "ok":
            s["ok"] += 1
            if r.get("correct"):
                s["correct"] += 1
        elif r["status"] == "tool_error":
            s["tool_error"] += 1
        else:
            s["exception"] += 1

    for s in by_model.values():
        total = s["total"] or 1
        s["ok_rate"] = round(s["ok"] / total, 4)
        s["accuracy"] = round(s["correct"] / total, 4)
    return by_model


def main():
    parser = argparse.ArgumentParser(
        description="Benchmark tool-calling with OpenAI/Gemini on sampled test_data.csv rows."
    )
    parser.add_argument("--csv-path", default=str(CSV_PATH_DEFAULT))
    parser.add_argument("--samples-per-calculator", type=int, default=5)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--tolerance", type=float, default=0.05)
    parser.add_argument("--max-workers", type=int, default=32)
    parser.add_argument("--providers", default="openai,gemini")
    parser.add_argument("--openai-models", default="gpt-4o-mini")
    parser.add_argument("--gemini-models", default="gemini-1.5-flash")
    parser.add_argument("--anthropic-models", default="claude-sonnet-4-5")
    parser.add_argument(
        "--output-jsonl",
        default=str(ROOT / "evaluation" / "outputs" / "tool_call_benchmark_results.jsonl"),
    )
    parser.add_argument(
        "--summary-json",
        default=str(ROOT / "evaluation" / "outputs" / "tool_call_benchmark_summary.json"),
    )
    args = parser.parse_args()

    run_compile_preflight()

    rows = load_rows(Path(args.csv_path))
    sampled_rows = sample_rows_per_calculator(rows, args.samples_per_calculator, args.seed)

    providers = [x.strip().lower() for x in args.providers.split(",") if x.strip()]
    openai_models = [x.strip() for x in args.openai_models.split(",") if x.strip()]
    gemini_models = [x.strip() for x in args.gemini_models.split(",") if x.strip()]
    anthropic_models = [x.strip() for x in args.anthropic_models.split(",") if x.strip()]

    clients: Dict[str, Any] = {}
    if "openai" in providers:
        clients["openai"] = OpenAIClient()
    if "gemini" in providers:
        clients["gemini"] = GeminiClient()
    if "anthropic" in providers:
        clients["anthropic"] = AnthropicClient()

    tasks = []
    for provider in providers:
        if provider == "openai":
            for m in openai_models:
                for row in sampled_rows:
                    tasks.append((provider, m, row))
        elif provider == "gemini":
            for m in gemini_models:
                for row in sampled_rows:
                    tasks.append((provider, m, row))
        elif provider == "anthropic":
            for m in anthropic_models:
                for row in sampled_rows:
                    tasks.append((provider, m, row))
        else:
            raise ValueError(f"Unsupported provider: {provider}")

    out_jsonl = Path(args.output_jsonl)
    out_jsonl.parent.mkdir(parents=True, exist_ok=True)
    summary_path = Path(args.summary_json)
    summary_path.parent.mkdir(parents=True, exist_ok=True)

    results: List[Dict[str, Any]] = []
    write_lock = threading.Lock()

    def _worker(provider: str, model: str, row: Dict[str, str]):
        return run_one(
            row=row,
            provider=provider,
            model=model,
            client=clients[provider],
            tolerance=args.tolerance,
        )

    with out_jsonl.open("w") as out_f, ThreadPoolExecutor(max_workers=args.max_workers) as ex:
        futures = [ex.submit(_worker, p, m, r) for (p, m, r) in tasks]
        for fut in as_completed(futures):
            rec = fut.result()
            results.append(rec)
            with write_lock:
                out_f.write(json.dumps(rec, ensure_ascii=False) + "\n")

    summary = {
        "num_sampled_rows": len(sampled_rows),
        "samples_per_calculator": args.samples_per_calculator,
        "seed": args.seed,
        "tolerance": args.tolerance,
        "max_workers": args.max_workers,
        "providers": providers,
        "openai_models": openai_models,
        "gemini_models": gemini_models,
        "anthropic_models": anthropic_models,
        "totals": summarize(results),
    }
    summary_path.write_text(json.dumps(summary, indent=2, ensure_ascii=False) + "\n")

    print(json.dumps(summary, indent=2, ensure_ascii=False))
    print(f"Wrote results JSONL: {out_jsonl}")
    print(f"Wrote summary JSON: {summary_path}")


if __name__ == "__main__":
    main()
