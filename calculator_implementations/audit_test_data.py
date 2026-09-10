"""
Audit script for MedCalc-Bench-Verified.

For every row in datasets/test_data.csv, re-runs the row's own calculator
implementation (calculator_implementations/*.py) against its "Relevant
Entities" and compares the recomputed answer to the stored "Ground Truth
Answer". Rows where the two disagree by more than a small tolerance are
printed, so they can be investigated as candidate data-quality issues.

Usage:
    cd calculator_implementations
    python audit_test_data.py [--calc-id ID] [--limit N]
"""
import argparse
import ast
import importlib.util
import json
import os
import sys

import pandas as pd
from rounding import round_number

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(SCRIPT_DIR)

with open(os.path.join(SCRIPT_DIR, "name_to_python.json")) as f:
    CALC_INFO = json.load(f)

_module_cache = {}


def load_module(file_path):
    if file_path not in _module_cache:
        if not os.path.isabs(file_path):
            file_path = os.path.join(SCRIPT_DIR, file_path)
        name = os.path.splitext(os.path.basename(file_path))[0]
        spec = importlib.util.spec_from_file_location(name, file_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        _module_cache[file_path] = module
    return _module_cache[file_path]


def build_input_parameters(calculator_id, relevant_entities):
    """Mirrors the mapping logic in generate_csv.py."""
    if calculator_id == 49:
        return dict(relevant_entities)

    calc_map = CALC_INFO[str(calculator_id)]
    input_parameters = {}
    for entity, value in relevant_entities.items():
        python_name = calc_map[entity]
        if value == "False":
            value = False
        elif value == "True":
            value = True
        input_parameters[python_name] = value
    return input_parameters


def try_float(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return None


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--calc-id", type=int, default=None,
                         help="Only audit this Calculator ID")
    parser.add_argument("--limit", type=int, default=None,
                         help="Only check the first N rows")
    parser.add_argument("--tol", type=float, default=1e-3,
                         help="Relative tolerance for numeric mismatches")
    parser.add_argument("--file", type=str, default="test_data.csv",
                         help="CSV file under datasets/ to audit")
    args = parser.parse_args()

    df = pd.read_csv(os.path.join(REPO_ROOT, "datasets", args.file))
    if args.limit:
        df = df.iloc[:args.limit]

    mismatches = []
    errors = []
    checked = 0

    for _, row in df.iterrows():
        calculator_id = int(float(row["Calculator ID"]))
        if args.calc_id is not None and calculator_id != args.calc_id:
            continue

        try:
            relevant_entities = ast.literal_eval(row["Relevant Entities"])
        except Exception as e:
            errors.append((row["Row Number"], calculator_id, f"bad Relevant Entities: {e}"))
            continue

        calc_map = CALC_INFO[str(calculator_id)]
        file_path = calc_map["file path"]
        explanation_func_name = calc_map["explanation function"]

        try:
            module = load_module(file_path)
            explanation_func = getattr(module, explanation_func_name)
            input_parameters = build_input_parameters(calculator_id, relevant_entities)
            func_output = explanation_func(input_parameters)
        except Exception as e:
            errors.append((row["Row Number"], calculator_id, f"{type(e).__name__}: {e}"))
            continue

        checked += 1
        recomputed = func_output["Answer"]
        stored = row["Ground Truth Answer"]

        if row["Category"] in ["lab test", "physical", "dosage"]:
            recomputed_val = try_float(recomputed)
            stored_val = try_float(stored)
            if recomputed_val is None or stored_val is None:
                errors.append((row["Row Number"], calculator_id,
                                f"non-numeric answer: recomputed={recomputed!r} stored={stored!r}"))
                continue
            recomputed_rounded = round_number(recomputed_val)
            denom = max(abs(stored_val), 1e-9)
            if abs(recomputed_rounded - stored_val) / denom > args.tol:
                mismatches.append((row["Row Number"], calculator_id, row["Calculator Name"],
                                    stored_val, recomputed_rounded))
        else:
            if str(recomputed).strip() != str(stored).strip():
                mismatches.append((row["Row Number"], calculator_id, row["Calculator Name"],
                                    stored, recomputed))

    print(f"Checked {checked} rows.")
    print(f"\n=== {len(mismatches)} MISMATCHES (recomputed answer != stored Ground Truth Answer) ===")
    for row_num, cid, cname, stored, recomputed in mismatches:
        print(f"Row {row_num}  CalcID {cid} ({cname}):  stored={stored!r}  recomputed={recomputed!r}")

    print(f"\n=== {len(errors)} ERRORS (could not recompute) ===")
    for row_num, cid, msg in errors:
        print(f"Row {row_num}  CalcID {cid}:  {msg}")


if __name__ == "__main__":
    main()
