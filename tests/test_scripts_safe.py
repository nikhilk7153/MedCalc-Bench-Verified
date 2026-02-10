from __future__ import annotations

import builtins
import io
import json
import runpy
import types
from pathlib import Path

import pytest


ORIGINAL_OPEN = builtins.open


class _WriteOnlyStringIO(io.StringIO):
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False


def _open_write_only(path, mode="r", *args, **kwargs):
    if "w" in mode or "a" in mode:
        return _WriteOnlyStringIO()
    return ORIGINAL_OPEN(path, mode, *args, **kwargs)


def test_generate_csv_runs_with_empty_frame(monkeypatch):
    pd = pytest.importorskip("pandas")
    root = Path(__file__).resolve().parents[1]
    path = root / "calculator_implementations" / "generate_csv.py"

    empty_df = pd.DataFrame(columns=[
        "Calculator ID",
        "Note Type",
        "Calculator Name",
        "Category",
        "Output Type",
        "Patient Note",
        "Note ID",
        "Relevant Entities",
        "Ground Truth Answer",
    ])

    monkeypatch.setattr(pd, "read_csv", lambda *args, **kwargs: empty_df)
    monkeypatch.setattr(pd.DataFrame, "to_csv", lambda self, *args, **kwargs: None)

    runpy.run_path(path)


def test_generate_one_shot_no_side_effects(monkeypatch):
    root = Path(__file__).resolve().parents[1]
    path = root / "calculator_implementations" / "generate_one_shot.py"

    monkeypatch.setattr(json, "load", lambda *args, **kwargs: {})
    monkeypatch.setattr(json, "dump", lambda *args, **kwargs: None)
    monkeypatch.setattr(builtins, "open", _open_write_only)

    runpy.run_path(path)


def test_synthesize_patient_note_functions(monkeypatch):
    root = Path(__file__).resolve().parents[1]
    path = root / "calculator_implementations" / "synthesize_patient_note.py"

    source = path.read_text()
    cutoff = source.find('with open(os.path.join(SCRIPT_DIR, "name_to_python.json")')
    if cutoff == -1:
        pytest.skip("Unable to locate safe execution cutoff for synthesize_patient_note.py")

    safe_source = source[:cutoff]
    ns = {"__file__": str(path)}
    code = compile(safe_source, str(path), "exec")
    exec(code, ns)

    # deterministic randomness for testing
    ns["random"].seed(1)
    month, day, year = ns["random_date"]()
    assert 1 <= month <= 12
    assert 1 <= day <= 31
    assert 2000 <= year <= 2024

    note, params = ns["estimated_date_calculator"]()
    assert "last menstrual period" in note
    assert 20 <= params["cycle_length"] <= 30
    assert "menstrual_date" in params

    note, params = ns["qt_interval_patient_notes_bazett"]()
    assert "QT interval" in note
    assert "heart_rate" in params and "qt_interval" in params


def test_synthesize_patient_note_target_weight_and_mme(monkeypatch):
    root = Path(__file__).resolve().parents[1]
    path = root / "calculator_implementations" / "synthesize_patient_note.py"

    source = path.read_text()
    cutoff = source.find('with open(os.path.join(SCRIPT_DIR, "name_to_python.json")')
    if cutoff == -1:
        pytest.skip("Unable to locate safe execution cutoff for synthesize_patient_note.py")

    safe_source = source[:cutoff]
    ns = {"__file__": str(path)}
    code = compile(safe_source, str(path), "exec")
    exec(code, ns)

    height_module = ns["height_conversion"]
    monkeypatch.setattr(
        height_module,
        "height_conversion_in",
        lambda args: height_module.height_conversion_explanation_in(args)[1],
        raising=False,
    )
    monkeypatch.setattr(
        height_module,
        "height_conversion_cm",
        lambda args: height_module.height_conversion_explanation_cm(args)[1],
        raising=False,
    )
    monkeypatch.setattr(
        height_module,
        "height_conversion",
        lambda args: height_module.height_conversion_explanation(args)[1],
        raising=False,
    )

    monkeypatch.setattr(ns["random"], "uniform", lambda *args, **kwargs: 1.8)

    monkeypatch.setattr(ns["random"], "choice", lambda seq: "cm")
    _, params = ns["target_weight"]()
    assert params["height"] == [180, "cm"]

    monkeypatch.setattr(ns["random"], "choice", lambda seq: "in")
    _, params = ns["target_weight"]()
    assert params["height"][1] == "in"

    monkeypatch.setattr(ns["random"], "choice", lambda seq: "m")
    _, params = ns["target_weight"]()
    assert params["height"] == [1.8, "m"]

    monkeypatch.setattr(ns["random"], "sample", lambda seq, count: ["FentaNYL buccal"])
    monkeypatch.setattr(ns["random"], "randint", lambda *args, **kwargs: 1)
    _, params = ns["mme_conversion"]()
    assert params["FentaNYL buccal Dose"][1] == "\u00b5g"


def test_synthesize_patient_note_random_date_february(monkeypatch):
    root = Path(__file__).resolve().parents[1]
    path = root / "calculator_implementations" / "synthesize_patient_note.py"

    source = path.read_text()
    cutoff = source.find('with open(os.path.join(SCRIPT_DIR, "name_to_python.json")')
    if cutoff == -1:
        pytest.skip("Unable to locate safe execution cutoff for synthesize_patient_note.py")

    safe_source = source[:cutoff]
    ns = {"__file__": str(path)}
    code = compile(safe_source, str(path), "exec")
    exec(code, ns)

    values = iter([2, 2024, 15])
    monkeypatch.setattr(ns["random"], "randint", lambda *args, **kwargs: next(values))
    month, day, year = ns["random_date"]()
    assert month == 2
    assert year == 2024
    assert 1 <= day <= 29

    values = iter([2, 2023, 14])
    monkeypatch.setattr(ns["random"], "randint", lambda *args, **kwargs: next(values))
    month, day, year = ns["random_date"]()
    assert month == 2
    assert year == 2023
    assert 1 <= day <= 28


def test_synthesize_patient_note_mme_two_instances(monkeypatch):
    root = Path(__file__).resolve().parents[1]
    path = root / "calculator_implementations" / "synthesize_patient_note.py"

    source = path.read_text()
    cutoff = source.find('with open(os.path.join(SCRIPT_DIR, "name_to_python.json")')
    if cutoff == -1:
        pytest.skip("Unable to locate safe execution cutoff for synthesize_patient_note.py")

    safe_source = source[:cutoff]
    ns = {"__file__": str(path)}
    code = compile(safe_source, str(path), "exec")
    exec(code, ns)

    monkeypatch.setattr(ns["random"], "sample", lambda seq, count: ["Codeine", "HYDROcodone"])
    values = iter([2, 1, 1, 1, 1])
    monkeypatch.setattr(ns["random"], "randint", lambda *args, **kwargs: next(values))

    note, params = ns["mme_conversion"]()
    assert "Codeine Dose" in params
    assert "HYDROcodone Dose" in params
    assert "time a day" in note


class _DummyLoader:
    def __init__(self, explain_name="explain"):
        self.explain_name = explain_name

    def exec_module(self, module):
        def explain(input_parameters):
            answer = -10 if input_parameters.get("negative") else 10
            return {"Explanation": "dummy", "Answer": answer}

        setattr(module, self.explain_name, explain)


def _patch_importlib_with_dummy(monkeypatch, explain_name="explain"):
    import importlib.util

    dummy_loader = _DummyLoader(explain_name)
    monkeypatch.setattr(
        importlib.util,
        "spec_from_file_location",
        lambda *args, **kwargs: types.SimpleNamespace(loader=dummy_loader),
    )
    monkeypatch.setattr(
        importlib.util,
        "module_from_spec",
        lambda *args, **kwargs: types.SimpleNamespace(),
    )


def test_generate_csv_branching(monkeypatch):
    pd = pytest.importorskip("pandas")
    root = Path(__file__).resolve().parents[1]
    path = root / "calculator_implementations" / "generate_csv.py"

    calc_info = {
        "24": {
            "question": "Q24?",
            "file path": "dummy.py",
            "explanation function": "explain",
            "calculator name": "Steroid Conversion",
            "type": "dosage",
            "input steroid": "input steroid",
            "target steroid": "target steroid",
            "negative": "negative",
        },
        "23": {
            "question": "Q23?",
            "file path": "dummy.py",
            "explanation function": "explain",
            "calculator name": "MELD Na",
            "type": "lab test",
            "entity A": "entity_a",
        },
        "68": {
            "question": "Q68?",
            "file path": "dummy.py",
            "explanation function": "explain",
            "calculator name": "Estimated Date of Conception",
            "type": "date",
            "Last menstrual date": "menstrual_date",
        },
        "49": {
            "question": "Q49?",
            "file path": "dummy.py",
            "explanation function": "explain",
            "calculator name": "MME",
            "type": "dosage",
        },
    }

    df = pd.DataFrame(
        [
            {
                "Calculator ID": 24,
                "Note Type": "Template",
                "Calculator Name": "Steroid Conversion",
                "Category": "dosage",
                "Output Type": "numeric",
                "Patient Note": "Template note",
                "Note ID": "note-24",
                "Relevant Entities": "{'input steroid': ['PredniSONE PO', 5, 'mg'], 'target steroid': 'Hydrocortisone IV', 'negative': 'True'}",
                "Ground Truth Answer": "0",
                "Question": "",
            },
            {
                "Calculator ID": 68,
                "Note Type": "Template",
                "Calculator Name": "Placeholder",
                "Category": "date",
                "Output Type": "date",
                "Patient Note": "LMP 01/01/2020",
                "Note ID": "note-68",
                "Relevant Entities": "{'Last menstrual date': '01/01/2020'}",
                "Ground Truth Answer": "01/15/2020",
                "Question": "",
            },
            {
                "Calculator ID": 23,
                "Note Type": "Synthetic",
                "Calculator Name": "MELD Na",
                "Category": "lab test",
                "Output Type": "numeric",
                "Patient Note": "Lab values",
                "Note ID": "note-23",
                "Relevant Entities": "{'entity A': 'False'}",
                "Ground Truth Answer": "999",
                "Question": "",
            },
            {
                "Calculator ID": 49,
                "Note Type": "Synthetic",
                "Calculator Name": "MME",
                "Category": "dosage",
                "Output Type": "numeric",
                "Patient Note": "Medication list",
                "Note ID": "note-49",
                "Relevant Entities": "{'negative': True}",
                "Ground Truth Answer": "-10",
                "Question": "",
            },
        ]
    )

    monkeypatch.setattr(pd, "read_csv", lambda *args, **kwargs: df)
    monkeypatch.setattr(pd.DataFrame, "to_csv", lambda self, *args, **kwargs: None)
    monkeypatch.setattr(json, "load", lambda *args, **kwargs: calc_info)
    _patch_importlib_with_dummy(monkeypatch, explain_name="explain")

    runpy.run_path(path)


def test_generate_csv_invalid_relevant_entities(monkeypatch):
    pd = pytest.importorskip("pandas")
    root = Path(__file__).resolve().parents[1]
    path = root / "calculator_implementations" / "generate_csv.py"

    calc_info = {
        "23": {
            "question": "Q23?",
            "file path": "dummy.py",
            "explanation function": "explain",
            "calculator name": "MELD Na",
            "type": "lab test",
            "entity A": "entity_a",
        }
    }

    df = pd.DataFrame(
        [
            {
                "Calculator ID": 23,
                "Note Type": "Synthetic",
                "Calculator Name": "MELD Na",
                "Category": "lab test",
                "Output Type": "numeric",
                "Patient Note": "Lab values",
                "Note ID": "note-23",
                "Relevant Entities": "{not valid}",
                "Ground Truth Answer": "999",
                "Question": "",
            }
        ]
    )

    monkeypatch.setattr(pd, "read_csv", lambda *args, **kwargs: df)
    monkeypatch.setattr(pd.DataFrame, "to_csv", lambda self, *args, **kwargs: None)
    monkeypatch.setattr(json, "load", lambda *args, **kwargs: calc_info)
    _patch_importlib_with_dummy(monkeypatch, explain_name="explain")

    with pytest.raises(Exception):
        runpy.run_path(path)


def test_generate_one_shot_updates_response(monkeypatch):
    root = Path(__file__).resolve().parents[1]
    path = root / "calculator_implementations" / "generate_one_shot.py"

    calc_info = {
        "1": {
            "file path": "dummy.py",
            "explanation function": "explain",
        }
    }
    one_shot_payload = {
        "1": {
            "input_parameters": {"negative": False},
            "Response": {"step_by_step_thinking": "", "answer": ""},
        }
    }
    dumped = {}

    def fake_json_load(file_obj, *args, **kwargs):
        if "name_to_python.json" in file_obj.name:
            return calc_info
        return one_shot_payload

    monkeypatch.setattr(json, "load", fake_json_load)
    monkeypatch.setattr(json, "dump", lambda data, *args, **kwargs: dumped.update({"data": data}))
    monkeypatch.setattr(builtins, "open", _open_write_only)
    _patch_importlib_with_dummy(monkeypatch, explain_name="explain")

    runpy.run_path(path)

    assert dumped["data"]["1"]["Response"]["answer"] == 10


def test_synthesize_patient_note_full_script(monkeypatch):
    root = Path(__file__).resolve().parents[1]
    path = root / "calculator_implementations" / "synthesize_patient_note.py"

    calc_ids = ["11", "13", "24", "56", "57", "58", "59", "61", "49", "68", "69"]
    calc_info = {
        calc_id: {
            "calculator name": f"calc-{calc_id}",
            "file path": "dummy.py",
            "explanation function": "explain",
        }
        for calc_id in calc_ids
    }

    def fake_json_load(file_obj, *args, **kwargs):
        return calc_info

    monkeypatch.setattr(json, "load", fake_json_load)
    monkeypatch.setattr(builtins, "open", _open_write_only)
    _patch_importlib_with_dummy(monkeypatch, explain_name="explain")

    import height_conversion as hc

    monkeypatch.setattr(
        hc,
        "height_conversion_in",
        lambda args: hc.height_conversion_explanation_in(args)[1],
        raising=False,
    )
    monkeypatch.setattr(
        hc,
        "height_conversion_cm",
        lambda args: hc.height_conversion_explanation_cm(args)[1],
        raising=False,
    )
    monkeypatch.setattr(
        hc,
        "height_conversion",
        lambda args: hc.height_conversion_explanation(args)[1],
        raising=False,
    )

    orig_range = range

    def tiny_range(*args):
        if args == (0, 100):
            return orig_range(0, 2)
        return orig_range(*args)

    monkeypatch.setattr(builtins, "range", tiny_range)

    runpy.run_path(path)
