from __future__ import annotations

import importlib.util
import sys
import types
from pathlib import Path

import pytest
import evaluate


def test_parse_first_number():
    if not hasattr(evaluate, "parse_first_number"):
        pytest.skip("parse_first_number is not exposed by this evaluate module revision")
    assert evaluate.parse_first_number("1,234.5 mg/dL") == 1234.5
    assert evaluate.parse_first_number("abc") is None


def test_round_half_up():
    if not hasattr(evaluate, "round_half_up"):
        pytest.skip("round_half_up is not exposed by this evaluate module revision")
    assert evaluate.round_half_up(2.5) == 3
    assert evaluate.round_half_up(-2.5) == -3


def test_check_correctness_date_and_tuple_and_decimal():
    assert evaluate.check_correctness("01/02/2024", "01/02/2024", 13, None, None) == 1
    assert evaluate.check_correctness("(3, 2)", "(3, 2)", 69, None, None) == 1
    # Decimal calculators are validated via bounds in this evaluate module.
    assert evaluate.check_correctness("3.4", "3.4", 2, "3.5", "3.3") == 1
    assert evaluate.check_correctness("1.05", "1.05", 2, "1.1", "1.0") == 1


def test_check_correctness_unknown_id():
    try:
        evaluate.check_correctness("1", "1", 999, None, None)
    except ValueError as exc:
        assert "Unknown calculator ID" in str(exc)
    else:
        raise AssertionError("Expected ValueError for unknown calculator ID")


def _load_eval_run_with_stub_llm():
    root = Path(__file__).resolve().parents[1]
    path = root / "evaluation" / "run.py"

    dummy_llm = types.SimpleNamespace(LLMInference=object)
    sys.modules.setdefault("llm_inference", dummy_llm)

    spec = importlib.util.spec_from_file_location("eval_run", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)  # type: ignore[arg-type]
    return module


def test_extract_answer_variants():
    eval_run = _load_eval_run_with_stub_llm()
    answer, _ = eval_run.extract_answer('{"answer": "1/2/2024"}', 13)
    assert answer == "01/02/2024"

    answer, _ = eval_run.extract_answer('{"answer": "(3 weeks, 2 days)"}', 69)
    assert answer == "(3, 2)"

    answer, _ = eval_run.extract_answer('{"answer": "3 out of 5"}', 4)
    assert answer == "3"

    answer, _ = eval_run.extract_answer('{"answer": "53.1%"}', 2)
    assert answer == "0.531"

    answer, _ = eval_run.extract_answer('{"answer": "str(2+3)"}', 2)
    assert answer == "5"

    answer, _ = eval_run.extract_answer('{"answer": "3, 4, 5"}', 4)
    assert answer == "3"

    answer, _ = eval_run.extract_answer('{"answer": "str(short_and_direct_answer_of_the_question)"}', 2)
    assert answer == "N/A"

    answer, _ = eval_run.extract_answer('{"answer": "13/40/2024"}', 13)
    assert answer == "N/A"


def _load_generate_code_prompt_with_stub_openai():
    root = Path(__file__).resolve().parents[1]
    path = root / "evaluation" / "generate_code_prompt.py"

    dummy_openai = types.SimpleNamespace()
    dummy_openai.api_key = None
    dummy_openai.ChatCompletion = types.SimpleNamespace(create=lambda **kwargs: None)

    sys.modules.setdefault("openai", dummy_openai)

    spec = importlib.util.spec_from_file_location("generate_code_prompt", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)  # type: ignore[arg-type]
    return module


def test_capture_exec_output_and_errors():
    module = _load_generate_code_prompt_with_stub_openai()
    output = module.capture_exec_output_and_errors("print('hi')")
    assert "hi" in output

    error_output = module.capture_exec_output_and_errors("1/0")
    assert "ZeroDivisionError" in error_output


def test_extract_python_code():
    module = _load_generate_code_prompt_with_stub_openai()
    text = "Here is code:\n```python\nprint('ok')\n```"
    assert module.extract_python_code(text).strip() == "print('ok')"
