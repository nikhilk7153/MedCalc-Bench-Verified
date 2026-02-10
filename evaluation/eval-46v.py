import argparse
import ast
import json
import math
import os
import re
import time
from pathlib import Path

import numpy as np
import pandas as pd
import tqdm
import openai
from jinja2 import Template

from evaluate import check_correctness
from table_stats import compute_overall_accuracy


# GLM Coding Plan endpoint (OpenAI-compatible) for GLM-4.6v
BASE_URL = ""
MODEL_NAME = "glm-4.6v"
BASE_DIR = Path(__file__).resolve().parent
CALC_DIR = BASE_DIR.parent / "calculator_implementations"

SYSTEM_PROMPT = (
    "You are a clinical extraction assistant. Use only the patient note. The calculator "
    "specification below is authoritative for parameters, units, conversions, and formula. "
    "Extract parameter values in canonical units. For each parameter, return an object with "
    "\"value\" and \"unit\". If a parameter is missing, set its value to null and note it in "
    "extraction_notes. If you can compute the final value, compute it; otherwise, set answer "
    "to \"N/A\". Output only a JSON object with the exact schema: "
    "{\"parameters\": {...}, \"extraction_notes\": [...], \"answer\": \"<value>\"} and nothing "
    "else. Keep \"answer\" as the last field in the JSON."
)

USER_TEMPLATE = Template(
    "Patient note:\n{{ note }}\n\n"
    "Calculator specification:\n{{ calculator_spec }}\n\n"
    "Task:\n{{ question }}\n\n"
    "Return only the JSON object."
)

CALC_INFO_PATH = CALC_DIR / "name_to_python.json"
CALC_METADATA_KEYS = {"file path", "explanation function", "calculator name", "type", "question"}


def configure_client():
    api_key = os.getenv("ZAI_API_KEY") or os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise SystemExit("Missing API key. Set ZAI_API_KEY (preferred) or OPENAI_API_KEY.")
    openai.api_key = api_key
    openai.api_base = BASE_URL


def call_glm(messages, max_retries=5):
    for attempt in range(1, max_retries + 1):
        try:
            return openai.ChatCompletion.create(
                model=MODEL_NAME,
                messages=messages,
            )
        except Exception as exc:
            if attempt >= max_retries:
                raise
            sleep_for = min(2 ** (attempt - 1), 20)
            print(f"Request failed ({exc}); retrying in {sleep_for}s...")
            time.sleep(sleep_for)


def zero_shot(note, question):
    system_msg = (
        'You are a helpful assistant for calculating a score for a given patient note. '
        'Please think step-by-step to solve the question and then generate the required score. '
        'Your output should only contain a JSON dict formatted as '
        '{"step_by_step_thinking": str(your_step_by_step_thinking_procress_to_solve_the_question), '
        '"answer": str(short_and_direct_answer_of_the_question)}.'
    )
    user_temp = (
        f'Here is the patient note:\n{note}\n\n'
        f'Here is the task:\n{question}\n\n'
        'Please directly output the JSON dict formatted as '
        '{"step_by_step_thinking": str(your_step_by_step_thinking_procress_to_solve_the_question), '
        '"answer": str(short_and_direct_answer_of_the_question)}:'
    )
    return system_msg, user_temp


def direct_answer(note, question):
    system_msg = (
        'You are a helpful assistant for calculating a score for a given patient note. '
        'Please output answer only without any other text. Your output should only contain '
        'a JSON dict formatted as {"answer": str(value which is the answer to the question)}.'
    )
    user_temp = (
        f'Here is the patient note:\n{note}\n\n'
        f'Here is the task:\n{question}\n\n'
        'Please directly output the JSON dict formatted as '
        '{"answer": str(value which is the answer to the question)}:'
    )
    return system_msg, user_temp


def one_shot(note, question, one_shot_question, example_note, example_output):
    system_msg = (
        'You are a helpful assistant for calculating a score for a given patient note. '
        'Please think step-by-step to solve the question and then generate the required score. '
        'Your output should only contain a JSON dict formatted as '
        '{"step_by_step_thinking": str(your_step_by_step_thinking_procress_to_solve_the_question), '
        '"answer": str(short_and_direct_answer_of_the_question)}.'
    )
    system_msg += f'Here is an example patient note:\n\n{example_note}'
    system_msg += f'\n\nHere is an example task:\n\n{one_shot_question}'
    system_msg += (
        '\n\nPlease directly output the JSON dict formatted as '
        '{"step_by_step_thinking": str(your_step_by_step_thinking_procress_to_solve_the_question), '
        '"answer": str(value which is the answer to the question)}:\n\n'
        f'{json.dumps(example_output)}'
    )
    user_temp = (
        f'Here is the patient note:\n\n{note}\n\n'
        f'Here is the task:\n\n{question}\n\n'
        'Please directly output the JSON dict formatted as '
        '{"step_by_step_thinking": str(your_step_by_step_thinking_procress_to_solve_the_question), '
        '"answer": str(short_and_direct_answer_of_the_question)}:'
    )
    return system_msg, user_temp


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


def load_module_source(module_name):
    module_path = CALC_DIR / f"{module_name}.py"
    if not module_path.exists():
        return None, None
    return module_name, module_path.read_text()


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
    imports = extract_local_imports(main_code)
    helper_sources = []
    seen_modules = set()
    for module in sorted(imports):
        if module in seen_modules:
            continue
        seen_modules.add(module)
        module_name, module_source = load_module_source(module)
        if module_name and module_source:
            helper_sources.append((module_name, module_source))

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


def extract_answer(answer, calid):
    calid = int(calid)
    extracted_answer = re.findall(r'[Aa]nswer":\s*(.*?)\}', answer)
    matches = re.findall(r'"step_by_step_thinking":\s*"([^"]+)"\s*,\s*"[Aa]nswer"', answer)

    if matches:
        explanation = matches[-1]
    else:
        explanation = "No Explanation"

    if len(extracted_answer) == 0:
        extracted_answer = "Not Found"
    else:
        extracted_answer = extracted_answer[-1].strip().strip('"')
        if extracted_answer in [
            "str(short_and_direct_answer_of_the_question)",
            "str(value which is the answer to the question)",
            "X.XX",
        ]:
            extracted_answer = "Not Found"

    if calid in [13, 68]:
        match = re.search(r"^(0?[1-9]|1[0-2])\/(0?[1-9]|[12][0-9]|3[01])\/(\d{4})", extracted_answer)
        if match:
            month = int(match.group(1))
            day = int(match.group(2))
            year = match.group(3)
            answer_value = f"{month:02}/{day:02}/{year}"
        else:
            answer_value = "N/A"

    elif calid in [69]:
        match = re.search(r"\(?[\"\']?(\d+)\s*(weeks?)?[\"\']?,?\s*[\"\']?(\d+)\s*(days?)?[\"\']?\s*\)?", extracted_answer)
        ground_truth = f"({match.group(1)}, {match.group(3)})"
        extracted_answer = extracted_answer.replace("[", "(").replace("]", ")").replace("'", "").replace('"', "")
        match = re.search(r"\(?[\"\']?(\d+)\s*(weeks?)?[\"\']?,?\s*[\"\']?(\d+)\s*(days?)?[\"\']?\s*\)?", extracted_answer)
        if match:
            weeks = match.group(1)
            days = match.group(3)
            answer_value = f"({weeks}, {days})"
        else:
            answer_value = "N/A"
    elif calid in [4, 15, 16, 17, 18, 20, 21, 25, 27, 28, 29, 32, 33, 36, 43, 45, 48, 51, 69]:
        match = re.search(r"(\d+) out of", extracted_answer)
        if match:
            answer_value = match.group(1)
        else:
            match = re.search(r"-?\d+(, ?-?\d+)+", extracted_answer)
            if match:
                answer_value = str(len(match.group(0).split(",")))
            else:
                match = re.findall(r"(-?\d+(\.\d+)?)", extracted_answer)
                if len(match) > 0:
                    answer_value = match[-1][0]
                else:
                    answer_value = "N/A"
    elif calid in [2, 3, 5, 6, 7, 8, 9, 10, 11, 19, 22, 23, 24, 26, 30, 31, 38, 39, 40, 44, 46, 49, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67]:
        match = re.search(r"str\((.*)\)", extracted_answer)
        if match:
            expression = match.group(1)
            expression = (
                expression.replace("^", "**")
                .replace("is odd", "% 2 == 1")
                .replace("is even", "% 2 == 0")
                .replace("sqrt", "math.sqrt")
                .replace(".math", "")
                .replace("weight", "")
                .replace("height", "")
                .replace("mg/dl", "")
                .replace("g/dl", "")
                .replace("mmol/L", "")
                .replace("kg", "")
                .replace("g", "")
                .replace("mEq/L", "")
            )
            expression = expression.split('#')[0]
            if expression.count('(') > expression.count(')'):
                expression += ')' * (expression.count('(') - expression.count(')'))
            elif expression.count(')') > expression.count('('):
                expression = '(' * (expression.count(')') - expression.count('(')) + expression
            try:
                answer_value = eval(
                    expression,
                    {"__builtins__": None},
                    {"min": min, "pow": pow, "round": round, "abs": abs, "int": int, "float": float, "math": math, "np": np, "numpy": np},
                )
            except Exception:
                print(f"Error in evaluating expression: {expression}")
                answer_value = "N/A"
        else:
            match = re.search(r"(-?\d+(\.\d+)?)\s*mL/min/1.73", extracted_answer)
            if match:
                answer_value = eval(match.group(1))
            else:
                match = re.findall(r"(-?\d+(\.\d+)?)\%", extracted_answer)
                if len(match) > 0:
                    answer_value = eval(match[-1][0]) / 100
                else:
                    match = re.findall(r"(-?\d+(\.\d+)?)", extracted_answer)
                    if len(match) > 0:
                        answer_value = eval(match[-1][0])
                    else:
                        answer_value = "N/A"
        if answer_value != "N/A":
            answer_value = str(answer_value)
    else:
        answer_value = "N/A"

    return answer_value, explanation


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


def resolve_data_path():
    return BASE_DIR.parent / "datasets" / "test_data.csv"


def load_one_shot_examples():
    with open(BASE_DIR / "one_shot_finalized_explanation.json", "r") as file:
        return json.load(file)


def main():
    parser = argparse.ArgumentParser(description="Run GLM-4.6v on MedCalc-Bench test_data.csv")
    parser.add_argument(
        "--prompt",
        type=str,
        default="calc_spec",
        choices=["direct_answer", "zero_shot", "one_shot", "calc_spec"],
        help="Prompt style to use.",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=None,
        help="Optional row limit for quick runs.",
    )
    args = parser.parse_args()

    os.chdir(BASE_DIR)
    configure_client()

    prompt_style = args.prompt
    output_tag = MODEL_NAME.replace("/", "_")
    output_path = f"{output_tag}_{prompt_style}.jsonl"

    outputs_dir = BASE_DIR / "outputs"
    outputs_dir.mkdir(exist_ok=True)

    existing = None
    output_file = outputs_dir / output_path
    if output_file.exists():
        existing = pd.read_json(output_file, lines=True)
        existing["Calculator ID"] = existing["Calculator ID"].astype(str)
        existing["Note ID"] = existing["Note ID"].astype(str)

    df = pd.read_csv(resolve_data_path())
    if args.limit is not None:
        df = df.head(args.limit)

    one_shot_json = None
    if prompt_style == "one_shot":
        one_shot_json = load_one_shot_examples()

    calc_metadata = None
    if prompt_style == "calc_spec":
        calc_metadata = load_calculator_metadata()

    for index in tqdm.tqdm(range(len(df))):
        row = df.iloc[index]

        patient_note = row["Patient Note"]
        question = row["Question"]
        calculator_id = str(row["Calculator ID"])
        note_id = str(row["Note ID"])

        if existing is not None:
            if existing[(existing["Calculator ID"] == calculator_id) & (existing["Note ID"] == str(row["Note ID"]))].shape[0] > 0:
                continue

        if prompt_style == "zero_shot":
            system, user = zero_shot(patient_note, question)
        elif prompt_style == "one_shot":
            if calculator_id == "24":
                one_shot_question = "Based on the patient's dose of Hydrocortisone IV, what is the equivalent dosage in mg of Dexamethasone PO?"
            else:
                one_shot_question = question
            example = one_shot_json[calculator_id]
            system, user = one_shot(
                patient_note,
                question,
                one_shot_question,
                example["Patient Note"],
                {
                    "step_by_step_thinking": example["Response"]["step_by_step_thinking"],
                    "answer": example["Response"]["answer"],
                },
            )
        elif prompt_style == "direct_answer":
            system, user = direct_answer(patient_note, question)
        else:
            calculator_spec = build_calculator_spec(calculator_id, calc_metadata)
            system = SYSTEM_PROMPT
            user = USER_TEMPLATE.render(
                note=patient_note,
                calculator_spec=calculator_spec,
                question=question,
            )

        messages = [
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ]

        response = call_glm(messages)
        answer_text = response.choices[0].message.content

        try:
            if prompt_style == "calc_spec":
                parsed = parse_json_response(answer_text)
                answer_value = parsed.get("answer", "N/A")
                if answer_value is None:
                    answer_value = "N/A"
                explanation = json.dumps(
                    {
                        "parameters": parsed.get("parameters"),
                        "extraction_notes": parsed.get("extraction_notes"),
                    },
                    ensure_ascii=False,
                )
                answer_value = str(answer_value)
            else:
                answer_value, explanation = extract_answer(answer_text, int(calculator_id))

            correctness = check_correctness(
                answer_value,
                row["Ground Truth Answer"],
                calculator_id,
                row["Upper Limit"],
                row["Lower Limit"],
            )
            status = "Correct" if correctness else "Incorrect"

            outputs = {
                "Row Number": int(row["Row Number"]),
                "Calculator Name": row["Calculator Name"],
                "Calculator ID": calculator_id,
                "Category": row["Category"],
                "Note ID": note_id,
                "Patient Note": patient_note,
                "Question": question,
                "LLM Answer": answer_value,
                "LLM Explanation": explanation,
                "Ground Truth Answer": row["Ground Truth Answer"],
                "Ground Truth Explanation": row["Ground Truth Explanation"],
                "Result": status,
            }

            if prompt_style == "direct_answer":
                outputs["LLM Explanation"] = "N/A"

        except Exception as exc:
            outputs = {
                "Row Number": int(row["Row Number"]),
                "Calculator Name": row["Calculator Name"],
                "Calculator ID": calculator_id,
                "Category": row["Category"],
                "Note ID": note_id,
                "Patient Note": patient_note,
                "Question": question,
                "LLM Answer": str(exc),
                "LLM Explanation": str(exc),
                "Ground Truth Answer": row["Ground Truth Answer"],
                "Ground Truth Explanation": row["Ground Truth Explanation"],
                "Result": "Incorrect",
            }
            if prompt_style == "direct_answer":
                outputs["LLM Explanation"] = "N/A"
            print(f"error in {calculator_id} {note_id}: {exc}")

        with open(output_file, "a") as file:
            file.write(json.dumps(outputs) + "\n")

    compute_overall_accuracy(output_path, MODEL_NAME, prompt_style)


if __name__ == "__main__":
    main()
