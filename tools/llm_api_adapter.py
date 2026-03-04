import ast
import importlib.util
import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CATALOG_PATH = ROOT / "tools" / "api_catalog.json"
TOOLS_DIR = ROOT / "tools"


def _load_catalog():
    return json.loads(CATALOG_PATH.read_text())


def _to_number(value):
    if isinstance(value, (int, float)):
        return float(value)
    if isinstance(value, str):
        return float(value.strip())
    raise ValueError(f"Cannot parse numeric value from {value!r}")


def _try_parse_structured_string(value):
    if not isinstance(value, str):
        return value
    text = value.strip()
    if not text:
        return value
    if text[0] in "[{(":
        for parser in (json.loads, ast.literal_eval):
            try:
                return parser(text)
            except Exception:
                continue
    return value


def _coerce_boolean(value):
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        v = value.strip().lower()
        if v in {"true", "t", "yes", "y", "1"}:
            return True
        if v in {"false", "f", "no", "n", "0"}:
            return False
    raise ValueError(f"Cannot coerce boolean from {value!r}")


def _coerce_number_unit(value):
    value = _try_parse_structured_string(value)

    if isinstance(value, (list, tuple)) and len(value) == 2:
        return [_to_number(value[0]), str(value[1])]

    if isinstance(value, dict):
        if "value" in value and "unit" in value:
            return [_to_number(value["value"]), str(value["unit"])]
        if len(value) == 1:
            k, v = next(iter(value.items()))
            return [_to_number(v), str(k)]

    if isinstance(value, str):
        # examples: "12 mg/dL", "98.6 degrees fahrenheit"
        m = re.match(r"^\s*([-+]?\d*\.?\d+(?:[eE][-+]?\d+)?)\s+(.+?)\s*$", value)
        if m:
            num, unit = m.groups()
            return [_to_number(num), unit]

    raise ValueError(f"Cannot coerce [number, unit] from {value!r} — the model must provide both a value and a unit")


def _coerce_by_schema(raw_value, schema):
    kind = schema.get("kind")
    fmt = schema.get("format")

    if kind == "numerical":
        if isinstance(fmt, list) and fmt == ["number", "unit"]:
            return _coerce_number_unit(raw_value)
        # format is ["number"] — return bare number (no unit conversion needed)
        parsed = _try_parse_structured_string(raw_value)
        return _to_number(parsed)

    # categorical
    possible = schema.get("possible_values")
    if isinstance(possible, list):
        if possible == [True, False]:
            return _coerce_boolean(raw_value)

        # string enum matching (case-insensitive)
        if isinstance(raw_value, str):
            for p in possible:
                if isinstance(p, str) and raw_value.strip().lower() == p.lower():
                    return p
        if raw_value in possible:
            return raw_value
        raise ValueError(f"Value {raw_value!r} not in allowed options: {possible!r}")

    # unconstrained categorical
    return raw_value


def get_api(calculator_id):
    normalized_id = str(calculator_id).strip()
    for api in _load_catalog():
        if str(api["calculator_id"]).strip() == normalized_id:
            return api
    raise KeyError(f"Calculator ID {calculator_id} not found in catalog")


def normalize_args(calculator_id, raw_args):
    api = get_api(calculator_id)
    normalized = {}
    errors = {}

    schema_by_name = {a["python_name"]: a for a in api["arguments"]}
    for name, arg_schema in schema_by_name.items():
        required = arg_schema.get("required", False)
        default = arg_schema.get("default")
        has_value = name in raw_args and raw_args[name] is not None

        if not has_value:
            if required:
                errors[name] = "missing required argument"
            else:
                normalized[name] = default  # passes None (or false/etc.) into the function
            continue

        try:
            normalized[name] = _coerce_by_schema(raw_args[name], arg_schema["schema"])
        except Exception as e:
            errors[name] = str(e)

    return normalized, errors, api


def invoke(calculator_id, raw_args):
    normalized, errors, api = normalize_args(calculator_id, raw_args)
    if errors:
        return {"ok": False, "errors": errors, "normalized_args": normalized}

    tools_dir_str = str(TOOLS_DIR)
    if tools_dir_str not in sys.path:
        sys.path.insert(0, tools_dir_str)

    module_path = TOOLS_DIR / api["tool_module"]
    mod_name = module_path.stem + "_runtime"
    try:
        spec = importlib.util.spec_from_file_location(mod_name, module_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        fn = getattr(module, api["function_name"])
        result = fn(**normalized)
    except Exception as exc:
        return {"ok": False, "errors": {"tool_execution": str(exc)}, "normalized_args": normalized}
    return {"ok": True, "result": result, "normalized_args": normalized}
