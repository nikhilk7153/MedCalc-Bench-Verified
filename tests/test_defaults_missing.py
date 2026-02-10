from __future__ import annotations

import pytest
import cardiac_risk_index
import caprini_score
import feverpain
import has_bled_score
import heart_score
import meldna
import perc_rule
import sirs_criteria
import sofa
import wells_criteria_pe
import glasgow_bleeding_score


def test_meldna_missing_flags_defaults():
    params = {
        "creatinine": [0.8, "mg/dL"],
        "bilirubin": [0.8, "mg/dL"],
        "inr": 0.9,
        "sodium": [140, "mEq/L"],
        "albumin": [4.0, "g/dL"],
        "age": [40, "years"],
        "sex": "Male",
    }
    result = meldna.compute_meldna_explanation(params)
    assert result["Answer"] == 6


def test_meldna_missing_albumin_errors():
    params = {
        "creatinine": [1.0, "mg/dL"],
        "bilirubin": [1.0, "mg/dL"],
        "inr": 1.0,
        "sodium": [137, "mEq/L"],
        "age": [40, "years"],
        "sex": "Male",
    }
    with pytest.raises(KeyError):
        meldna.compute_meldna_explanation(params)


def test_sofa_defaults_for_ventilation_and_gcs():
    params = {
        "pao2": [150, "mm Hg"],
        "fio2": [100, "%"],
        "platelet_count": [200000, "µL"],
        "bilirubin": [1.0, "mg/dL"],
        "creatinine": [1.0, "mg/dL"],
    }
    result = sofa.compute_sofa_explanation(params)
    assert result["Answer"] == 2


def test_heart_score_defaults_to_low_risk():
    params = {"age": [30, "years"]}
    result = heart_score.compute_heart_score_explanation(params)
    assert result["Answer"] == 0


def test_caprini_defaults_no_extra_points():
    params = {"sex": "Male", "age": [40, "years"]}
    result = caprini_score.caprini_score_explanation(params)
    assert result["Answer"] == 0


def test_cardiac_risk_index_missing_creatinine():
    result = cardiac_risk_index.compute_cardiac_index_explanation({})
    assert result["Answer"] == 0


def test_sirs_missing_resp_and_paco2_defaults():
    params = {
        "temperature": [98.6, "degrees fahrenheit"],
        "heart_rate": [80, "beats/min"],
        "wbc": [8000, "mm^3"],
    }
    result = sirs_criteria.sirs_criteria_explanation(params)
    assert result["Answer"] == 0


def test_perc_rule_missing_history_defaults():
    params = {
        "age": [49, "years"],
        "heart_rate": [90, "beats/min"],
        "oxygen_sat": [98, "%"],
    }
    result = perc_rule.compute_perc_rule_explanation(params)
    assert result["Answer"] == 0


def test_wells_pe_missing_history_defaults():
    params = {"heart_rate": [80, "beats/min"]}
    result = wells_criteria_pe.calculate_pe_wells_explanation(params)
    assert result["Answer"] == 0


def test_has_bled_defaults_no_flags():
    params = {"age": [30, "years"], "alcoholic_drinks": "0"}
    result = has_bled_score.compute_has_bled_score_explanation(params)
    assert result["Answer"] == 0


def test_feverpain_missing_cough_adds_point():
    params = {
        "fever_24_hours": False,
        "symptom_onset": False,
        "purulent_tonsils": False,
        "severe_tonsil_inflammation": False,
    }
    result = feverpain.compute_fever_pain_explanation(params)
    assert result["Answer"] == 0


def test_glasgow_bleeding_defaults_missing_flags():
    params = {
        "hemoglobin": [14.0, "g/dL"],
        "bun": [10.0, "mg/dL"],
        "sex": "Male",
        "sys_bp": [120, "mm Hg"],
        "heart_rate": [80, "beats/min"],
    }
    result = glasgow_bleeding_score.glasgow_bleeding_score_explanation(params)
    assert result["Answer"] == 0
