import importlib.util
import json
import os
import copy

# Get the directory where this script is located
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)

# Use the full path to name_to_python.json
with open(os.path.join(SCRIPT_DIR, "name_to_python.json"), "r") as f:
    calc_info = json.load(f)

with open(os.path.join(PROJECT_ROOT, "evaluation", "one_shot_finalized_explanation.json"), "r") as f:
    one_shot_finalized_explanation = json.load(f)

def get_explanation(calculator_id, input_parameters, calc_info):
    """
    Get explanation and answer for a calculator given its input parameters
    """
    # Get the file path and explanation function name
    relative_file_path = calc_info[str(calculator_id)]["file path"]
    explanation_func_name = calc_info[str(calculator_id)]["explanation function"]
    
    # Construct the full path by joining with calculator_implementations directory
    file_path = os.path.join(SCRIPT_DIR, relative_file_path)
    
    # Get just the filename without path and extension
    file_name = os.path.splitext(os.path.basename(file_path))[0]
    
    # Import the module dynamically
    spec = importlib.util.spec_from_file_location(file_name, file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    
    # Get the explanation function
    explanation_func = getattr(module, explanation_func_name)
    
    # Call the explanation function with input parameters
    return explanation_func(input_parameters)


# For each calculator in the synthetic instances:
for calc_id, instance in one_shot_finalized_explanation.items():
    print(calc_id)
    # Make a deep copy to prevent the explanation function from modifying the original
    input_params = copy.deepcopy(instance["input_parameters"])
    result = get_explanation(calc_id, input_params, calc_info)
   
    one_shot_finalized_explanation[calc_id]["Response"]["step_by_step_thinking"] = result["Explanation"]
    one_shot_finalized_explanation[calc_id]["Response"]["answer"] = result["Answer"]

with open(os.path.join(PROJECT_ROOT, "evaluation", "one_shot_finalized_explanation.json"), "w") as f:
    json.dump(one_shot_finalized_explanation, f, indent=4)