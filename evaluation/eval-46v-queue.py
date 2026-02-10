import argparse
import ast
import csv
import importlib.util
import json
import math
import os
import queue as queue_module
import random
import re
import sys
import time
import traceback
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd
import openai
from jinja2 import Template

from evaluate import check_correctness
from table_stats import compute_overall_accuracy


BASE_URL = ""
DEFAULT_MODEL = "glm-4.6v"
BASE_DIR = Path(__file__).resolve().parent
CALC_DIR = BASE_DIR.parent / "calculator_implementations"
CALC_INFO_PATH = CALC_DIR / "name_to_python.json"
CALC_METADATA_KEYS = {"file path", "explanation function", "calculator name", "type", "question"}
PROMPTS_DIR = BASE_DIR / "prompts"

SYSTEM_PROMPT_DEFAULT = (
    "You are a clinical extraction assistant. Use only the patient note. The calculator "
    "specification below is authoritative for parameters, units, conversions, and formula. "
    "Extract parameter values in canonical units. For each parameter, return an object with "
    "\"value\" and \"unit\". If a parameter is missing, set its value to null and note it in "
    "extraction_notes. If you can compute the final value, compute it; otherwise, set answer "
    "to \"N/A\". Output only a JSON object with the exact schema: "
    "{\"parameters\": {...}, \"extraction_notes\": [...], \"answer\": \"<value>\"} and nothing "
    "else. Keep \"answer\" as the last field in the JSON."
)

USER_TEMPLATE_DEFAULT = (
    "Patient note:\n{{ note }}\n\n"
    "Calculator specification:\n{{ calculator_spec }}\n\n"
    "Task:\n{{ question }}\n\n"
    "Return only the JSON object."
)


def configure_client():
    api_key = os.getenv("ZAI_API_KEY") or os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise SystemExit("Missing API key. Set ZAI_API_KEY (preferred) or OPENAI_API_KEY.")
    openai.api_key = api_key
    openai.api_base = BASE_URL


def log(message):
    timestamp = datetime.now(timezone.utc).isoformat()
    print(f"[{timestamp}] {message}", flush=True)


def call_glm(messages, model_name, max_retries=5, log_requests=False, semaphore=None):
    attempts = 0
    for attempt in range(1, max_retries + 1):
        attempts = attempt
        acquired = False
        if semaphore is not None:
            semaphore.acquire()
            acquired = True
        try:
            if log_requests:
                log(f"Request attempt {attempt}: sending to {model_name}.")
            response = openai.ChatCompletion.create(
                model=model_name,
                messages=messages,
            )
            if log_requests:
                log(f"Request attempt {attempt}: received response.")
            return response, attempts
        except Exception as exc:
            if attempt >= max_retries:
                raise
            sleep_for = min(2 ** (attempt - 1), 20)
            sleep_for += random.uniform(0, 0.5)
            log(f"Request failed ({exc}); retrying in {sleep_for:.1f}s...")
            time.sleep(sleep_for)
        finally:
            if acquired and semaphore is not None:
                semaphore.release()
    return None, attempts


def load_calculator_metadata():
    with open(CALC_INFO_PATH, "r") as file:
        return json.load(file)


def extract_local_imports(code_text):
    imports = set()
    try:
        tree = ast.parse(code_text)
    except SyntaxError:
        return imports

    for node in tree.body:
        if isinstance(node, ast.Import):
            for alias in node.names:
                imports.add(alias.name.split(".")[0])
        elif isinstance(node, ast.ImportFrom) and node.module:
            imports.add(node.module.split(".")[0])

    return imports


def collect_module_sources(module_name, collected, seen):
    if module_name in seen:
        return
    seen.add(module_name)
    module_path = CALC_DIR / f"{module_name}.py"
    if not module_path.exists():
        return
    module_source = module_path.read_text()
    collected.append((module_name, module_source))
    for dep in extract_local_imports(module_source):
        collect_module_sources(dep, collected, seen)


def build_calculator_spec(calculator_id, calc_metadata):
    calc_id = str(calculator_id)
    calc_info = calc_metadata.get(calc_id)
    if not calc_info:
        return f"Calculator ID {calc_id} not found in name_to_python.json."

    file_path = calc_info.get("file path")
    if not file_path:
        return f"Calculator ID {calc_id} has no file path in name_to_python.json."

    file_path = Path(file_path)
    if not file_path.is_absolute():
        file_path = CALC_DIR / file_path

    if not file_path.exists():
        return f"Calculator file not found: {file_path}"

    main_code = file_path.read_text()
    main_module = file_path.stem

    helper_sources = []
    seen_modules = {main_module}
    for module in extract_local_imports(main_code):
        collect_module_sources(module, helper_sources, seen_modules)

    param_lines = []
    for key, value in calc_info.items():
        if key in CALC_METADATA_KEYS:
            continue
        param_lines.append(f"- {key} -> {value}")

    spec_lines = [
        f"Calculator ID: {calc_id}",
        f"Calculator Name: {calc_info.get('calculator name', 'N/A')}",
        f"Category: {calc_info.get('type', 'N/A')}",
        f"Canonical Question: {calc_info.get('question', 'N/A')}",
        "",
        "Parameters (patient note label -> canonical name):",
        *param_lines,
        "",
        f"Implementation file: {file_path}",
        "Implementation (authoritative source code):",
        "```python",
        main_code,
        "```",
    ]

    if helper_sources:
        spec_lines.extend(["", "Referenced helper modules (authoritative source code):"])
        for module_name, module_source in helper_sources:
            spec_lines.extend(
                [
                    f"Module: {module_name}.py",
                    "```python",
                    module_source,
                    "```",
                ]
            )

    return "\n".join(spec_lines)


def parse_json_response(text):
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        start = text.find("{")
        end = text.rfind("}")
        if start == -1 or end == -1 or end <= start:
            return {}
        try:
            return json.loads(text[start : end + 1])
        except json.JSONDecodeError:
            return {}


def resolve_data_path(path_value):
    path = Path(path_value)
    if not path.is_absolute():
        path = (BASE_DIR / path).resolve()
    return path


def sanitize_filename(value):
    return re.sub(r"[^A-Za-z0-9._-]+", "_", str(value))


def make_task_id(row):
    row_number = row["Row Number"]
    calc_id = row["Calculator ID"]
    note_id = row["Note ID"]
    return f"row{row_number}_calc{calc_id}_note{sanitize_filename(note_id)}"


def serialize_response(response):
    if response is None:
        return None
    if hasattr(response, "to_dict_recursive"):
        return response.to_dict_recursive()
    try:
        return json.loads(json.dumps(response))
    except TypeError:
        return {"repr": repr(response)}


def build_prompt_payload(messages, task_id, job_id, prompt_id, model_name):
    return {
        "task_id": task_id,
        "job_id": job_id,
        "prompt_id": prompt_id,
        "model": model_name,
        "base_url": BASE_URL,
        "messages": messages,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


def load_prompt_def(prompt_id):
    if prompt_id is None:
        return {
            "id": "calc_spec",
            "schema": "calc_spec_full",
            "has_answer": True,
            "system": SYSTEM_PROMPT_DEFAULT,
            "user": USER_TEMPLATE_DEFAULT,
        }

    prompt_path = PROMPTS_DIR / f"{prompt_id}.json"
    if not prompt_path.exists():
        raise SystemExit(f"Prompt file not found: {prompt_path}")
    with open(prompt_path, "r") as file:
        prompt_def = json.load(file)

    prompt_def.setdefault("id", prompt_id)
    prompt_def.setdefault("schema", prompt_id)
    prompt_def.setdefault("has_answer", True)
    if "system" not in prompt_def or "user" not in prompt_def:
        raise SystemExit(f"Prompt {prompt_id} must define 'system' and 'user' fields.")
    return prompt_def


def render_messages(prompt_def, note, calculator_spec, question):
    system_template = Template(prompt_def["system"])
    user_template = Template(prompt_def["user"])
    system_text = system_template.render(note=note, calculator_spec=calculator_spec, question=question)
    user_text = user_template.render(note=note, calculator_spec=calculator_spec, question=question)
    return [
        {"role": "system", "content": system_text},
        {"role": "user", "content": user_text},
    ]


def extract_fields(schema, response_text):
    parsed = parse_json_response(response_text)
    return {
        "schema": schema,
        "answer": parsed.get("answer"),
        "parameters_dataset": parsed.get("parameters_dataset"),
        "parameters": parsed.get("parameters"),
        "extraction_notes": parsed.get("extraction_notes"),
        "calculation_notes": parsed.get("calculation_notes"),
        "raw_text": response_text,
    }


def worker_loop(
    worker_id,
    task_queue,
    result_queue,
    prompt_def,
    model_name,
    max_retries,
    job_id,
    task_log_every,
    log_requests,
    semaphore,
):
    configure_client()
    calc_metadata = load_calculator_metadata()
    spec_cache = {}
    processed = 0
    log(f"Worker {worker_id} started for job {job_id}.")

    while True:
        task = task_queue.get()
        if task is None:
            result_queue.put({"_type": "DONE"})
            log(f"Worker {worker_id} done for job {job_id}.")
            break

        task_id = make_task_id(task)
        processed += 1
        if task_log_every and processed % task_log_every == 0:
            log(f"Worker {worker_id} processing task {processed} (task_id={task_id}).")
        calculator_id = str(task["Calculator ID"])
        note_id = str(task["Note ID"])
        patient_note = task["Patient Note"]
        question = task["Question"]

        prompt_payload = None
        response_raw = None
        error_info = None
        extract_info = None
        output_record = None
        timing = {"worker_id": worker_id}

        try:
            if calculator_id not in spec_cache:
                spec_cache[calculator_id] = build_calculator_spec(calculator_id, calc_metadata)
            calculator_spec = spec_cache[calculator_id]

            messages = render_messages(prompt_def, patient_note, calculator_spec, question)
            prompt_payload = build_prompt_payload(messages, task_id, job_id, prompt_def["id"], model_name)

            start_time = time.time()
            response, attempts = call_glm(
                messages,
                model_name,
                max_retries=max_retries,
                log_requests=log_requests,
                semaphore=semaphore,
            )
            end_time = time.time()
            timing.update({"start": start_time, "end": end_time, "latency_s": end_time - start_time, "attempts": attempts})

            response_raw = serialize_response(response)
            answer_text = response_raw.get("choices", [{}])[0].get("message", {}).get("content", "")

            extract_info = extract_fields(prompt_def.get("schema"), answer_text)

            answer_value = extract_info.get("answer")
            if answer_value is None:
                answer_value = "N/A"
            answer_value = str(answer_value)

            has_answer = bool(prompt_def.get("has_answer", True))
            if has_answer:
                if answer_value == "N/A":
                    status = "Incorrect"
                else:
                    correctness = check_correctness(
                        answer_value,
                        task["Ground Truth Answer"],
                        calculator_id,
                        task["Upper Limit"],
                        task["Lower Limit"],
                    )
                    status = "Correct" if correctness else "Incorrect"
            else:
                status = "N/A"

            output_record = {
                "Task ID": task_id,
                "Job ID": job_id,
                "Prompt ID": prompt_def["id"],
                "Row Number": int(task["Row Number"]),
                "Calculator Name": task["Calculator Name"],
                "Calculator ID": calculator_id,
                "Category": task["Category"],
                "Note ID": note_id,
                "Patient Note": patient_note,
                "Question": question,
                "LLM Answer": answer_value,
                "LLM Explanation": json.dumps(
                    {
                        "extraction_notes": extract_info.get("extraction_notes"),
                        "parameters_dataset": extract_info.get("parameters_dataset"),
                        "parameters": extract_info.get("parameters"),
                        "calculation_notes": extract_info.get("calculation_notes"),
                    },
                    ensure_ascii=False,
                ),
                "Ground Truth Answer": task["Ground Truth Answer"],
                "Ground Truth Explanation": task["Ground Truth Explanation"],
                "Lower Limit": task["Lower Limit"],
                "Upper Limit": task["Upper Limit"],
                "Result": status,
            }
        except Exception as exc:
            error_info = {
                "task_id": task_id,
                "job_id": job_id,
                "error": str(exc),
                "traceback": traceback.format_exc(),
                "worker_id": worker_id,
            }
            output_record = {
                "Task ID": task_id,
                "Job ID": job_id,
                "Prompt ID": prompt_def["id"],
                "Row Number": int(task["Row Number"]),
                "Calculator Name": task["Calculator Name"],
                "Calculator ID": calculator_id,
                "Category": task["Category"],
                "Note ID": note_id,
                "Patient Note": patient_note,
                "Question": question,
                "LLM Answer": str(exc),
                "LLM Explanation": str(exc),
                "Ground Truth Answer": task["Ground Truth Answer"],
                "Ground Truth Explanation": task["Ground Truth Explanation"],
                "Lower Limit": task["Lower Limit"],
                "Upper Limit": task["Upper Limit"],
                "Result": "Incorrect",
            }
            log(f"Worker {worker_id} error in {calculator_id} {note_id}: {exc}")

        result_queue.put(
            {
                "_type": "RESULT",
                "task_id": task_id,
                "job_id": job_id,
                "prompt_id": prompt_def["id"],
                "task": task,
                "prompt": prompt_payload,
                "response": response_raw,
                "extract": extract_info,
                "output": output_record,
                "error": error_info,
                "timing": timing,
            }
        )


def write_json_atomic(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp_path = path.with_suffix(path.suffix + ".tmp")
    with open(tmp_path, "w") as file:
        json.dump(data, file, ensure_ascii=False)
    os.replace(tmp_path, path)


def load_existing(output_file):
    if not output_file.exists():
        return set()
    if output_file.stat().st_size == 0:
        return set()
    try:
        existing = pd.read_json(output_file, lines=True)
    except ValueError:
        return set()
    if "Calculator ID" not in existing.columns or "Note ID" not in existing.columns:
        return set()
    existing = existing.copy()
    existing.loc[:, "Calculator ID"] = existing["Calculator ID"].astype(str)
    existing.loc[:, "Note ID"] = existing["Note ID"].astype(str)
    return set(zip(existing["Calculator ID"], existing["Note ID"]))


def normalize_list_value(value, python_name=None):
    if not isinstance(value, list) or len(value) != 2:
        return value
    if python_name and python_name.lower() in {"sex", "gender"}:
        return value[0]
    unit = value[1]
    if isinstance(unit, str):
        unit_lower = unit.lower()
        if any(token in unit_lower for token in ("bool", "category", "categorical", "sex", "gender")):
            return value[0]
    return value


def to_input_parameters_from_dataset(parameters_dataset, calc_info):
    input_params = {}
    if not isinstance(parameters_dataset, dict):
        return input_params
    param_keys = {key for key in calc_info if key not in CALC_METADATA_KEYS and key.lower() != "question"}
    allow_passthrough = not param_keys
    for entity_name, value in parameters_dataset.items():
        if value is None:
            continue
        if isinstance(value, str) and value in ("True", "False"):
            value = value == "True"
        python_name = calc_info.get(entity_name)
        if python_name:
            input_params[python_name] = normalize_list_value(value, python_name)
        elif allow_passthrough:
            input_params[entity_name] = normalize_list_value(value, entity_name)
    return input_params


def to_input_parameters_from_canonical(parameters):
    input_params = {}
    if not isinstance(parameters, dict):
        return input_params
    for python_name, value in parameters.items():
        if value is None:
            continue
        if isinstance(value, dict) and "value" in value and "unit" in value:
            unit = value.get("unit")
            if isinstance(unit, str) and ("bool" in unit or "category" in unit):
                extracted = value.get("value")
                if isinstance(extracted, str) and extracted in ("True", "False"):
                    extracted = extracted == "True"
                input_params[python_name] = extracted
            else:
                input_params[python_name] = [value.get("value"), value.get("unit")]
        else:
            if isinstance(value, str) and value in ("True", "False"):
                value = value == "True"
            input_params[python_name] = value
    return input_params


def compute_answer_from_params(calculator_id, parameters_dataset, parameters, calc_metadata, module_cache):
    calc_id = str(calculator_id)
    calc_info = calc_metadata.get(calc_id)
    if not calc_info:
        return None, "calculator_not_found"

    input_params = to_input_parameters_from_dataset(parameters_dataset, calc_info)
    if not input_params:
        input_params = to_input_parameters_from_canonical(parameters)

    if not input_params:
        return None, "no_parameters"

    file_path = calc_info.get("file path")
    if not file_path:
        return None, "missing_file_path"

    file_path = Path(file_path)
    if not file_path.is_absolute():
        file_path = CALC_DIR / file_path

    if not file_path.exists():
        return None, f"missing_file:{file_path}"

    module_key = str(file_path)
    module = module_cache.get(module_key)
    if module is None:
        calc_dir_str = str(CALC_DIR)
        if calc_dir_str not in sys.path:
            sys.path.insert(0, calc_dir_str)
        spec = importlib.util.spec_from_file_location(file_path.stem, file_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        module_cache[module_key] = module

    func_name = calc_info.get("explanation function")
    if not func_name or not hasattr(module, func_name):
        return None, "missing_explanation_function"

    explanation_func = getattr(module, func_name)
    try:
        output = explanation_func(input_params)
    except Exception as exc:
        return None, f"compute_error:{exc}"
    answer = output.get("Answer") if isinstance(output, dict) else None
    if answer is None:
        return None, "no_answer"
    return str(answer), None


def consolidate_run(run_dir, calc_metadata):
    run_dir = Path(run_dir)
    outputs_file = run_dir / "outputs.jsonl"
    combined_file = run_dir / "combined.jsonl"
    results_csv = run_dir / "results.csv"

    if not outputs_file.exists():
        print(f"No outputs.jsonl found in {run_dir}")
        return

    module_cache = {}

    with open(outputs_file, "r") as infile, open(combined_file, "w") as combined:
        rows = []
        for line in infile:
            if not line.strip():
                continue
            record = json.loads(line)
            task_id = record.get("Task ID") or make_task_id(record)

            prompt_path = run_dir / "prompts" / f"{task_id}.json"
            response_path = run_dir / "responses" / f"{task_id}.json"
            extract_path = run_dir / "extracts" / f"{task_id}.json"
            error_path = run_dir / "errors" / f"{task_id}.json"
            timing_path = run_dir / "timing" / f"{task_id}.json"

            prompt = json.load(open(prompt_path)) if prompt_path.exists() else None
            response = json.load(open(response_path)) if response_path.exists() else None
            extract = json.load(open(extract_path)) if extract_path.exists() else None
            error = json.load(open(error_path)) if error_path.exists() else None
            timing = json.load(open(timing_path)) if timing_path.exists() else None

            combined_record = {
                "output": record,
                "prompt": prompt,
                "response": response,
                "extract": extract,
                "error": error,
                "timing": timing,
            }
            combined.write(json.dumps(combined_record, ensure_ascii=False) + "\n")

            parameters_dataset = extract.get("parameters_dataset") if extract else None
            parameters = extract.get("parameters") if extract else None
            extraction_notes = extract.get("extraction_notes") if extract else None
            answer = extract.get("answer") if extract else None
            latency_s = timing.get("latency_s") if timing else None
            attempts = timing.get("attempts") if timing else None
            worker_id = timing.get("worker_id") if timing else None

            computed_answer = None
            computed_error = None
            computed_status = "N/A"
            if parameters_dataset or parameters:
                computed_answer, computed_error = compute_answer_from_params(
                    record.get("Calculator ID"),
                    parameters_dataset,
                    parameters,
                    calc_metadata,
                    module_cache,
                )
                if computed_answer is not None:
                    correctness = check_correctness(
                        str(computed_answer),
                        record.get("Ground Truth Answer"),
                        record.get("Calculator ID"),
                        record.get("Upper Limit"),
                        record.get("Lower Limit"),
                    )
                    computed_status = "Correct" if correctness else "Incorrect"

            status = record.get("Result")
            if status == "N/A" and computed_status != "N/A":
                status = computed_status

            rows.append(
                {
                    "row_number": record.get("Row Number"),
                    "calc_id": record.get("Calculator ID"),
                    "note_id": record.get("Note ID"),
                    "question": record.get("Question"),
                    "extracted_answer": answer,
                    "extracted_parameters_dataset": json.dumps(parameters_dataset, ensure_ascii=False),
                    "extracted_parameters": json.dumps(parameters, ensure_ascii=False),
                    "extraction_notes": json.dumps(extraction_notes, ensure_ascii=False),
                    "ground_truth_answer": record.get("Ground Truth Answer"),
                    "ground_truth_explanation": record.get("Ground Truth Explanation"),
                    "lower_limit": record.get("Lower Limit"),
                    "upper_limit": record.get("Upper Limit"),
                    "computed_answer": computed_answer,
                    "computed_status": computed_status,
                    "computed_error": computed_error,
                    "status": status,
                    "latency_s": latency_s,
                    "attempts": attempts,
                    "worker_id": worker_id,
                }
            )

    with open(results_csv, "w", newline="") as csvfile:
        fieldnames = [
            "row_number",
            "calc_id",
            "note_id",
            "question",
            "extracted_answer",
            "extracted_parameters_dataset",
            "extracted_parameters",
            "extraction_notes",
            "ground_truth_answer",
            "ground_truth_explanation",
            "lower_limit",
            "upper_limit",
            "computed_answer",
            "computed_status",
            "computed_error",
            "status",
            "latency_s",
            "attempts",
            "worker_id",
        ]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def write_progress(run_dir, written, done_workers, queued_total=None, last_write_utc=None, last_error=None, last_event=None):
    payload = {
        "written": written,
        "done_workers": done_workers,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
    if queued_total is not None:
        payload["queued_total"] = queued_total
    if last_write_utc:
        payload["last_write_utc"] = last_write_utc
    if last_error:
        payload["last_error"] = last_error
    if last_event:
        payload["last_event"] = last_event
    write_json_atomic(Path(run_dir) / "progress.json", payload)


def writer_loop(
    result_queue,
    output_file,
    output_path,
    model_name,
    prompt_def,
    worker_count,
    run_dir,
    job_id,
    progress_every,
    queued_total,
    heartbeat_seconds,
):
    os.chdir(BASE_DIR)
    outputs_dir = Path(output_file).parent
    outputs_dir.mkdir(parents=True, exist_ok=True)

    run_dir = Path(run_dir)
    run_outputs_file = run_dir / "outputs.jsonl"

    progress_every = max(1, int(progress_every))
    results_written = 0
    done_count = 0
    last_write_time = None
    last_write_utc = None
    last_error = None
    last_event = "start"
    write_progress(run_dir, results_written, done_count, queued_total, last_write_utc, last_error, last_event)

    with open(output_file, "a") as file, open(run_outputs_file, "a") as run_file:
        last_heartbeat = time.time()
        while done_count < worker_count:
            try:
                item = result_queue.get(timeout=heartbeat_seconds)
            except queue_module.Empty:
                now = time.time()
                if now - last_heartbeat >= heartbeat_seconds:
                    age = None if last_write_time is None else round(now - last_write_time, 1)
                    log(
                        "Job {}: heartbeat - written {}, done workers {}/{}, last_write_age_s={}, queued_total={}".format(
                            job_id,
                            results_written,
                            done_count,
                            worker_count,
                            age,
                            queued_total,
                        )
                    )
                    last_event = "heartbeat"
                    write_progress(run_dir, results_written, done_count, queued_total, last_write_utc, last_error, last_event)
                    last_heartbeat = now
                continue
            if isinstance(item, dict) and item.get("_type") == "DONE":
                done_count += 1
                last_event = "worker_done"
                write_progress(run_dir, results_written, done_count, queued_total, last_write_utc, last_error, last_event)
                log(f"Job {job_id}: worker finished ({done_count}/{worker_count}).")
                continue
            if not isinstance(item, dict) or item.get("_type") != "RESULT":
                continue

            task_id = item.get("task_id")
            if item.get("task"):
                write_json_atomic(run_dir / "tasks" / f"{task_id}.json", item["task"])
            if item.get("prompt"):
                write_json_atomic(run_dir / "prompts" / f"{task_id}.json", item["prompt"])
            if item.get("response") is not None:
                write_json_atomic(run_dir / "responses" / f"{task_id}.json", item["response"])
            if item.get("extract") is not None:
                write_json_atomic(run_dir / "extracts" / f"{task_id}.json", item["extract"])
            if item.get("error") is not None:
                error_payload = item["error"] or {}
                last_error = {
                    "task_id": error_payload.get("task_id"),
                    "worker_id": error_payload.get("worker_id"),
                    "error": error_payload.get("error"),
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                }
                write_json_atomic(run_dir / "errors" / f"{task_id}.json", item["error"])
            if item.get("timing") is not None:
                write_json_atomic(run_dir / "timing" / f"{task_id}.json", item["timing"])

            output_record = item.get("output")
            if output_record is not None:
                file.write(json.dumps(output_record, ensure_ascii=False) + "\n")
                run_file.write(json.dumps(output_record, ensure_ascii=False) + "\n")
                results_written += 1
                last_write_time = time.time()
                last_write_utc = datetime.now(timezone.utc).isoformat()
                last_event = "write"
                if results_written % progress_every == 0:
                    file.flush()
                    run_file.flush()
                    write_progress(run_dir, results_written, done_count, queued_total, last_write_utc, last_error, last_event)
                    log(f"Job {job_id}: wrote {results_written} results (done workers: {done_count}/{worker_count}).")

    if prompt_def.get("has_answer", True):
        compute_overall_accuracy(output_path, model_name, prompt_def.get("schema", prompt_def["id"]))


def write_run_metadata(run_dir, args, job, queued_count, total_rows):
    metadata = {
        "run_id": Path(run_dir).name,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "model": job.get("model", DEFAULT_MODEL),
        "base_url": BASE_URL,
        "prompt_id": job["prompt_id"],
        "schema": job.get("schema"),
        "workers": job["workers"],
        "max_retries": job["max_retries"],
        "queue_size": job["queue_size"],
        "max_inflight": job.get("max_inflight"),
        "limit": job.get("limit"),
        "total_rows": total_rows,
        "queued_rows": queued_count,
        "dataset_path": job["dataset_path"],
        "resume": job["resume"],
        "progress_every": job["progress_every"],
    }
    write_json_atomic(Path(run_dir) / "run.json", metadata)


def build_job_configs(args, jobs_file):
    if jobs_file:
        with open(jobs_file, "r") as file:
            config = json.load(file)
        defaults = config.get("defaults", {})
        jobs = config.get("jobs", [])
        if not jobs:
            raise SystemExit("Jobs file contains no jobs.")
    else:
        defaults = {}
        jobs = [
            {
                "id": args.run_id or "calc_spec",
                "prompt_id": args.prompt,
                "dataset_path": args.dataset_path,
                "output_dir": args.output_dir,
                "limit": args.limit,
            }
        ]

    merged_jobs = []
    for job in jobs:
        merged = {}
        merged.update(defaults)
        merged.update(job)
        merged.setdefault("id", merged.get("prompt_id", "job"))
        merged.setdefault("prompt_id", "calc_spec")
        merged.setdefault("dataset_path", "../datasets/test_data.csv")
        merged.setdefault("output_dir", "logs/runs")
        merged.setdefault("model", getattr(args, "model", DEFAULT_MODEL))
        merged.setdefault("workers", 9)
        merged.setdefault("queue_size", 32)
        merged.setdefault("max_retries", 5)
        merged.setdefault("resume", True)
        merged.setdefault("progress_every", args.progress_every)
        merged.setdefault("heartbeat_seconds", args.heartbeat_seconds)
        merged.setdefault("task_log_every", args.task_log_every)
        merged.setdefault("log_requests", args.log_requests)
        merged.setdefault("max_inflight", args.max_inflight)
        merged_jobs.append(merged)

    return merged_jobs


def run_job(job, args, calc_metadata):
    model_name = str(job.get("model", DEFAULT_MODEL))
    model_key = model_name.lower()
    if model_key == "glm-4.7":
        # Provider limit: glm-4.7 must be strictly sequential (no parallel in-flight requests).
        if job.get("workers") != 1 or job.get("max_inflight") not in (None, 1):
            log(f"Job {job.get('id')}: forcing workers=1 and max_inflight=1 for model {model_name}.")
        job["workers"] = 1
        job["max_inflight"] = 1

    if job["workers"] > 9:
        raise SystemExit("workers > 9 exceeds the requested safety limit.")
    if job.get("max_inflight") is None:
        job["max_inflight"] = job["workers"]
    if job["max_inflight"] > 9:
        raise SystemExit("max_inflight > 9 exceeds the requested safety limit.")

    prompt_def = load_prompt_def(job["prompt_id"])
    log(
        "Starting job {} (model={}, prompt={}, dataset={}, workers={}, max_inflight={}).".format(
            job["id"],
            model_name,
            prompt_def["id"],
            job["dataset_path"],
            job["workers"],
            job["max_inflight"],
        )
    )

    dataset_path = resolve_data_path(job["dataset_path"])
    df = pd.read_csv(dataset_path)
    total_rows = len(df)
    if job.get("limit") is not None:
        df = df.head(job["limit"])

    output_tag = model_name.replace("/", "_")
    output_path = f"{output_tag}_{job['prompt_id']}_{job['id']}.jsonl"
    output_file = BASE_DIR / "outputs" / output_path

    existing = load_existing(output_file) if job.get("resume", True) else set()
    if existing:
        log(f"Job {job['id']}: resume enabled, {len(existing)} existing rows detected.")

    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    run_id = job.get("run_id") or f"{timestamp}_{output_tag}_{job['prompt_id']}_{job['id']}"
    run_dir = BASE_DIR / job["output_dir"] / run_id
    run_dir.mkdir(parents=True, exist_ok=True)

    ctx = __import__("multiprocessing").get_context("spawn")
    task_queue = ctx.Queue(maxsize=job["queue_size"])
    result_queue = ctx.Queue()
    api_semaphore = ctx.Semaphore(job["max_inflight"])

    tasks = []
    for _, row in df.iterrows():
        calc_id = str(row["Calculator ID"])
        note_id = str(row["Note ID"])
        if (calc_id, note_id) in existing:
            continue
        tasks.append(row.to_dict())

    queued = len(tasks)

    writer = ctx.Process(
        target=writer_loop,
        args=(
            result_queue,
            output_file,
            output_path,
            model_name,
            prompt_def,
            job["workers"],
            run_dir,
            job["id"],
            job["progress_every"],
            queued,
            job["heartbeat_seconds"],
        ),
    )
    writer.start()

    workers = []
    for idx in range(job["workers"]):
        proc = ctx.Process(
            target=worker_loop,
            args=(
                idx,
                task_queue,
                result_queue,
                prompt_def,
                model_name,
                job["max_retries"],
                job["id"],
                job["task_log_every"],
                job["log_requests"],
                api_semaphore,
            ),
        )
        proc.start()
        workers.append(proc)

    write_json_atomic(
        run_dir / "pids.json",
        {
            "main_pid": os.getpid(),
            "writer_pid": writer.pid,
            "worker_pids": [proc.pid for proc in workers],
            "timestamp": datetime.now(timezone.utc).isoformat(),
        },
    )

    for task in tasks:
        task_queue.put(task)

    write_run_metadata(run_dir, args, job, queued, total_rows)
    log(f"Job {job['id']}: queued {queued} tasks (total rows: {total_rows}).")

    for _ in range(job["workers"]):
        task_queue.put(None)

    for proc in workers:
        proc.join()

    writer.join()

    if not args.no_consolidate:
        consolidate_run(run_dir, calc_metadata)

    log(f"Job {job['id']} queued {queued} tasks. Results written to {output_file}.")
    log(f"Run logs: {run_dir}")


def main():
    parser = argparse.ArgumentParser(description="Run Z.AI OpenAI-compatible models with a multi-job queue runner.")
    parser.add_argument(
        "--model",
        type=str,
        default=DEFAULT_MODEL,
        help="Model name (used for single-job runs; jobs manifest can override).",
    )
    parser.add_argument(
        "--prompt",
        type=str,
        default="calc_spec",
        help="Prompt id (used for single-job runs).",
    )
    parser.add_argument(
        "--dataset-path",
        type=str,
        default="../datasets/test_data.csv",
        help="Dataset CSV path (used for single-job runs).",
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        default="logs/runs",
        help="Output directory for run logs (used for single-job runs).",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=None,
        help="Optional row limit for quick runs.",
    )
    parser.add_argument(
        "--workers",
        type=int,
        default=9,
        help="Number of parallel worker processes (max 9 recommended).",
    )
    parser.add_argument(
        "--max-retries",
        type=int,
        default=5,
        help="Max retries per request.",
    )
    parser.add_argument(
        "--queue-size",
        type=int,
        default=32,
        help="Task queue size.",
    )
    parser.add_argument(
        "--progress-every",
        type=int,
        default=25,
        help="Emit progress log/update every N results.",
    )
    parser.add_argument(
        "--heartbeat-seconds",
        type=int,
        default=30,
        help="Emit heartbeat progress log/update every N seconds (writer loop).",
    )
    parser.add_argument(
        "--task-log-every",
        type=int,
        default=50,
        help="Log every N tasks per worker (0 disables).",
    )
    parser.add_argument(
        "--log-requests",
        action="store_true",
        help="Log request start/end for each API call.",
    )
    parser.add_argument(
        "--max-inflight",
        type=int,
        default=None,
        help="Maximum number of concurrent API calls (defaults to workers).",
    )
    parser.add_argument(
        "--run-id",
        type=str,
        default=None,
        help="Optional run identifier for logs.",
    )
    parser.add_argument(
        "--jobs",
        type=str,
        default=None,
        help="Path to JSON job manifest for multiple runs.",
    )
    parser.add_argument(
        "--no-consolidate",
        action="store_true",
        help="Skip consolidation step (combined.jsonl/results.csv).",
    )
    args = parser.parse_args()

    try:
        log("Starting eval queue runner.")
        log(f"Args: {args}")
        calc_metadata = load_calculator_metadata()
        jobs = build_job_configs(args, args.jobs)
        log(f"Loaded {len(jobs)} job(s).")

        for job in jobs:
            job.setdefault("workers", args.workers)
            job.setdefault("queue_size", args.queue_size)
            job.setdefault("max_retries", args.max_retries)
            job.setdefault("resume", True)
            job.setdefault("progress_every", args.progress_every)
            run_job(job, args, calc_metadata)
    except Exception as exc:
        log(f"Fatal error: {exc}")
        log(traceback.format_exc())
        raise


if __name__ == "__main__":
    main()
