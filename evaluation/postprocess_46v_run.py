import argparse
import csv
import importlib.util
import json
import re
import sys
from pathlib import Path

from evaluate import check_correctness

BASE_DIR = Path(__file__).resolve().parent
CALC_DIR = BASE_DIR.parent / "calculator_implementations"
CALC_INFO_PATH = CALC_DIR / "name_to_python.json"
CALC_METADATA_KEYS = {"file path", "explanation function", "calculator name", "type", "question"}


def sanitize_filename(value):
    return re.sub(r"[^A-Za-z0-9._-]+", "_", str(value))


def make_task_id(row):
    row_number = row.get("Row Number") or row.get("row_number")
    calc_id = row.get("Calculator ID") or row.get("calc_id")
    note_id = row.get("Note ID") or row.get("note_id")
    return f"row{row_number}_calc{calc_id}_note{sanitize_filename(note_id)}"


def load_calculator_metadata():
    with open(CALC_INFO_PATH, "r") as file:
        return json.load(file)


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
            input_params[python_name] = value
        elif allow_passthrough:
            input_params[entity_name] = value
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
    output = explanation_func(input_params)
    answer = output.get("Answer") if isinstance(output, dict) else None
    if answer is None:
        return None, "no_answer"
    return str(answer), None


def consolidate_run(run_dir):
    run_dir = Path(run_dir)
    outputs_file = run_dir / "outputs.jsonl"
    combined_file = run_dir / "combined.jsonl"
    results_csv = run_dir / "results.csv"

    if not outputs_file.exists():
        raise SystemExit(f"No outputs.jsonl found in {run_dir}")

    calc_metadata = load_calculator_metadata()
    module_cache = {}

    rows = []
    with open(outputs_file, "r") as infile, open(combined_file, "w") as combined:
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

    print(f"Wrote {combined_file} and {results_csv}")


def main():
    parser = argparse.ArgumentParser(description="Consolidate atomic log files into combined.jsonl and results.csv")
    parser.add_argument("run_dir", type=str, help="Path to the run directory")
    args = parser.parse_args()
    consolidate_run(args.run_dir)


if __name__ == "__main__":
    main()
