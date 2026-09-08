import importlib.util
import json
import os
import ast

import pandas as pd

# Get the directory where this script is located
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)

ONE_SHOT_CSV = os.path.join(PROJECT_ROOT, "datasets", "one_shot_data.csv")
ONE_SHOT_JSON = os.path.join(PROJECT_ROOT, "evaluation", "one_shot_finalized_explanation.json")

# Use the full path to name_to_python.json
with open(os.path.join(SCRIPT_DIR, "name_to_python.json"), "r") as f:
    calc_info = json.load(f)

_module_cache = {}


def get_explanation(calculator_id, input_parameters, calc_info):
    """
    Get explanation and answer for a calculator given its input parameters
    """
    # Get the file path and explanation function name
    relative_file_path = calc_info[str(calculator_id)]["file path"]
    explanation_func_name = calc_info[str(calculator_id)]["explanation function"]

    # Construct the full path by joining with calculator_implementations directory
    file_path = os.path.join(SCRIPT_DIR, relative_file_path)

    if file_path not in _module_cache:
        # Get just the filename without path and extension
        file_name = os.path.splitext(os.path.basename(file_path))[0]

        # Import the module dynamically
        spec = importlib.util.spec_from_file_location(file_name, file_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        _module_cache[file_path] = module

    # Get the explanation function
    explanation_func = getattr(_module_cache[file_path], explanation_func_name)

    # Call the explanation function with input parameters
    return explanation_func(input_parameters)


def build_input_parameters(calculator_id, relevant_entities):
    """Map a row's Relevant Entities onto the calculator's python parameter
    names. Mirrors the mapping logic in generate_csv.py, including its
    special case for calculator 49, so the one-shot exemplars are built the
    same way as the dataset rows themselves."""
    if int(calculator_id) == 49:
        return dict(relevant_entities)

    calc_map = calc_info[str(calculator_id)]
    input_parameters = {}
    for entity, value in relevant_entities.items():
        python_name = calc_map[entity]
        if value == "False":
            value = False
        elif value == "True":
            value = True
        input_parameters[python_name] = value
    return input_parameters


def coerce_answer(stored_answer):
    """Keep the exemplar's answer identical in value to the dataset's stored
    Ground Truth Answer, preserving its numeric-vs-string form."""
    try:
        float(stored_answer)
    except (TypeError, ValueError):
        return stored_answer
    return float(stored_answer) if "." in stored_answer else int(stored_answer)


# The one-shot split is the single source of truth: the exemplar JSON that
# run.py prompts with is derived from it, never maintained alongside it.
one_shot_data = pd.read_csv(ONE_SHOT_CSV, dtype=str)

one_shot_finalized_explanation = {}

for _, row in one_shot_data.iterrows():
    calc_id = str(int(row["Calculator ID"]))
    print(calc_id)

    relevant_entities = ast.literal_eval(row["Relevant Entities"])
    input_parameters = build_input_parameters(calc_id, relevant_entities)

    result = get_explanation(calc_id, build_input_parameters(calc_id, relevant_entities), calc_info)

    # The recomputed explanation must agree with the one stored in the split;
    # if it does not, the split and the calculators have drifted apart and the
    # exemplar would silently teach something the dataset does not contain.
    if result["Explanation"].strip() != row["Ground Truth Explanation"].strip():
        raise ValueError(
            f"calculator {calc_id}: recomputed explanation does not match "
            f"one_shot_data.csv; regenerate the split before the exemplars"
        )

    one_shot_finalized_explanation[calc_id] = {
        "Response": {
            "step_by_step_thinking": row["Ground Truth Explanation"],
            "answer": coerce_answer(row["Ground Truth Answer"]),
        },
        "Patient Note": row["Patient Note"],
        "input_parameters": input_parameters,
    }

with open(ONE_SHOT_JSON, "w") as f:
    json.dump(one_shot_finalized_explanation, f, indent=4)
    f.write("\n")
