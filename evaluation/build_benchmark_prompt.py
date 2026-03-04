import argparse
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CATALOG_PATH = ROOT / "tools" / "api_catalog.json"
TOOLS_DIR = ROOT / "tools"


PROMPT_TEMPLATE = """You are given one medical calculator API.
Your task is to produce a valid tool call JSON for this calculator only.

Rules:
1) Use ONLY the provided calculator API and its schema.
2) Map patient/context inputs to the calculator arguments.
3) If required information is missing, still return JSON and set missing fields to null.
4) Do NOT add extra keys.
5) Output MUST be valid JSON only (no markdown, no explanation).

Expected output format:
{{
  "calculator_id": <int>,
  "arguments": {{
    "<python_arg_name>": <value or null>
  }}
}}

Notes on numeric fields:
- If schema.format is ["number"], return a scalar number.
- If schema.format is ["number", "unit"], return [number, "unit"].
- Respect schema.possible_values for categorical fields.

=== CALCULATOR API CATALOG ENTRY ===
{catalog_entry_json}

=== CALCULATOR API CODE ({tool_module}) ===
```python
{tool_code}
```

=== TASK INPUT ===
{task_input}

Return only the JSON object now.
"""


def load_catalog():
    return json.loads(CATALOG_PATH.read_text())


def get_entry(catalog, calculator_id):
    for entry in catalog:
        if int(entry["calculator_id"]) == int(calculator_id):
            return entry
    raise KeyError(f"calculator_id={calculator_id} not found in {CATALOG_PATH}")


def build_prompt(calculator_id, task_input):
    catalog = load_catalog()
    entry = get_entry(catalog, calculator_id)

    tool_module = entry["tool_module"]
    code_path = TOOLS_DIR / tool_module
    tool_code = code_path.read_text()

    return PROMPT_TEMPLATE.format(
        catalog_entry_json=json.dumps(entry, indent=2, ensure_ascii=False),
        tool_module=tool_module,
        tool_code=tool_code,
        task_input=task_input.strip(),
    )


def main():
    parser = argparse.ArgumentParser(
        description="Build a per-calculator benchmark prompt with API code + catalog entry."
    )
    parser.add_argument("--calculator-id", type=int, required=True)
    parser.add_argument(
        "--task-input",
        type=str,
        required=True,
        help="Patient/context text or JSON string to include under TASK INPUT.",
    )
    parser.add_argument(
        "--output",
        type=str,
        default="",
        help="Optional output file path. If omitted, prints to stdout.",
    )
    args = parser.parse_args()

    prompt = build_prompt(args.calculator_id, args.task_input)
    if args.output:
        out_path = Path(args.output)
        out_path.write_text(prompt)
        print(f"Wrote prompt: {out_path}")
    else:
        print(prompt)


if __name__ == "__main__":
    main()
