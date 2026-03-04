import argparse
import ast
import csv
import importlib.util
import inspect
import json
from collections import defaultdict
from pathlib import Path
import sys


def load_module(calc_dir: Path, file_name: str):
    module_path = calc_dir / file_name
    module_name = module_path.stem.replace("-", "_") + "_tolerance_check"
    spec = importlib.util.spec_from_file_location(module_name, module_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def to_prefix(drug_name: str) -> str:
    return drug_name.lower().replace(" ", "_").replace("-", "_")


def to_float(value):
    try:
        return float(value)
    except Exception:
        return None


def normalize_non_numeric(value):
    if isinstance(value, tuple):
        return tuple(str(x).strip().lower() for x in value)
    if isinstance(value, list):
        return [str(x).strip().lower() for x in value]
    return str(value).strip().lower()


def translate_entities(calc_id: str, entities: dict, name_to_python: dict) -> dict:
    mapping = name_to_python.get(calc_id, {})
    translated = dict(entities)

    for english_key, py_name in mapping.items():
        if english_key in {
            "file path",
            "explanation function",
            "calculator name",
            "type",
            "question",
            "Question",
        }:
            continue
        if english_key in entities:
            translated[py_name] = entities[english_key]

    # Keep compatibility with known typo in metadata.
    if "doboutamine" in translated and "dobutamine" not in translated:
        translated["dobutamine"] = translated["doboutamine"]

    return translated


def build_kwargs(nonexp_name: str, params: dict) -> dict:
    kwargs = dict(params)

    if nonexp_name == "caprini_score":
        if "surgery_type" in kwargs:
            kwargs["surgery_type_value"] = kwargs.pop("surgery_type")
        if "mobility" in kwargs:
            kwargs["mobility_value"] = kwargs.pop("mobility")

    if nonexp_name == "mme":
        mme_kwargs = {}
        for key in params:
            if key.endswith(" Dose"):
                drug = key[:-5]
                dose_per_day_key = f"{drug} Dose Per Day"
                if dose_per_day_key in params:
                    prefix = to_prefix(drug)
                    mme_kwargs[f"{prefix}_dose"] = params[key]
                    mme_kwargs[f"{prefix}_dose_per_day"] = params[dose_per_day_key]
        kwargs = mme_kwargs

    if nonexp_name == "compute_steroid_conversion":
        if "input steroid" in params and "target steroid" in params:
            kwargs = {
                "input_steroid": params["input steroid"],
                "target_steroid": params["target steroid"],
            }

    if nonexp_name == "apache_ii" and "mean_arterial_pressure" in kwargs:
        kwargs.pop("mean_arterial_pressure", None)

    return kwargs


def fill_required_with_defaults(signature: inspect.Signature, kwargs: dict) -> dict:
    # Keep only user-provided values; do not invent defaults.
    # If a required argument is missing, the calculator call should fail naturally.
    _ = signature
    return dict(kwargs)


def main():
    parser = argparse.ArgumentParser(
        description="Check calculator outputs against test_data ground truth."
    )
    parser.add_argument(
        "--repo-root",
        default=".",
        help="Path to repository root (default: current directory).",
    )
    parser.add_argument(
        "--csv-path",
        default="datasets/test_data.csv",
        help="Path to test CSV relative to repo root.",
    )
    parser.add_argument(
        "--tolerance",
        type=float,
        default=0.05,
        help="Relative tolerance for numeric outputs (default: 0.05 for 5%%).",
    )
    args = parser.parse_args()

    root = Path(args.repo_root).resolve()
    calc_dir = root / "calculator_implementations"
    csv_path = root / args.csv_path
    name_to_python_path = calc_dir / "name_to_python.json"

    sys.path.insert(0, str(calc_dir))
    name_to_python = json.loads(name_to_python_path.read_text())

    rows = []
    with open(csv_path, newline="") as f:
        reader = csv.DictReader(f)
        rows.extend(reader)

    module_cache = {}
    summary = defaultdict(lambda: {"total": 0, "pass": 0, "fail": 0, "errors": 0})
    overall = {"total": 0, "pass": 0, "fail": 0, "errors": 0}
    fail_examples = []
    error_examples = []

    for row in rows:
        calc_id = str(row["Calculator ID"]).strip()
        calc_name = row["Calculator Name"]
        calc_key = f"{calc_id} | {calc_name}"

        meta = name_to_python.get(calc_id)
        if not meta:
            summary[calc_key]["errors"] += 1
            overall["errors"] += 1
            continue

        exp_name = meta.get("explanation function")
        if not exp_name or not exp_name.endswith("_explanation"):
            summary[calc_key]["errors"] += 1
            overall["errors"] += 1
            continue
        nonexp_name = exp_name[:-12]
        file_path = meta.get("file path")

        try:
            entities = ast.literal_eval(row["Relevant Entities"])
            if not isinstance(entities, dict):
                raise ValueError("Relevant Entities is not a dict")
            translated = translate_entities(calc_id, entities, name_to_python)
        except Exception as exc:
            summary[calc_key]["errors"] += 1
            overall["errors"] += 1
            error_examples.append(
                (row["Row Number"], calc_key, f"entities parse/translate: {exc}")
            )
            continue

        try:
            if file_path not in module_cache:
                module_cache[file_path] = load_module(calc_dir, file_path)
            module = module_cache[file_path]
            fn = getattr(module, nonexp_name)
        except Exception as exc:
            summary[calc_key]["errors"] += 1
            overall["errors"] += 1
            error_examples.append((row["Row Number"], calc_key, f"load fn: {exc}"))
            continue

        try:
            sig = inspect.signature(fn)
            kwargs = build_kwargs(nonexp_name, translated)
            kwargs = {k: v for k, v in kwargs.items() if k in sig.parameters}
            kwargs = fill_required_with_defaults(sig, kwargs)
            prediction = fn(**kwargs)
        except Exception as exc:
            summary[calc_key]["errors"] += 1
            overall["errors"] += 1
            error_examples.append((row["Row Number"], calc_key, f"run: {exc}"))
            continue

        gt_raw = row["Ground Truth Answer"]
        gt_num = to_float(gt_raw)
        pred_num = to_float(prediction)

        passed = False
        if gt_num is not None and pred_num is not None:
            if gt_num == 0:
                passed = abs(pred_num - gt_num) <= args.tolerance
            else:
                rel_err = abs(pred_num - gt_num) / abs(gt_num)
                passed = rel_err <= args.tolerance
        else:
            gt_value = gt_raw
            try:
                gt_value = ast.literal_eval(gt_raw)
            except Exception:
                pass
            passed = normalize_non_numeric(prediction) == normalize_non_numeric(gt_value)

        summary[calc_key]["total"] += 1
        overall["total"] += 1

        if passed:
            summary[calc_key]["pass"] += 1
            overall["pass"] += 1
        else:
            summary[calc_key]["fail"] += 1
            overall["fail"] += 1
            fail_examples.append((row["Row Number"], calc_key, gt_raw, prediction))

    pass_rate = (overall["pass"] / overall["total"] * 100) if overall["total"] else 0.0

    print("OVERALL")
    print(json.dumps(overall, indent=2))
    print(f"pass_rate={pass_rate:.2f}%")
    print()

    print("PER_CALC")
    for calc_key in sorted(summary):
        s = summary[calc_key]
        if s["total"] == 0 and s["errors"] == 0:
            continue
        print(json.dumps({"calculator": calc_key, **s}))

    print()
    print("FAIL_EXAMPLES")
    for item in fail_examples:
        print(item)

    print()
    print("ERROR_EXAMPLES")
    for item in error_examples:
        print(item)


if __name__ == "__main__":
    main()
