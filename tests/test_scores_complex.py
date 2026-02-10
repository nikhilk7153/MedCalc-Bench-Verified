from __future__ import annotations

import math

import pytest

from rounding import round_number
import apache_ii
import psi_score
import sofa
import framingham_risk_score


def apache_base_params():
    return {
        "age": [30, "years"],
        "sex": "Male",
        "sodium": [140, "mmol/L"],
        "pH": 7.4,
        "heart_rate": [80, "beats/min"],
        "respiratory_rate": [16, "breaths/min"],
        "potassium": [4.0, "mmol/L"],
        "creatinine": [1.0, "mg/dL"],
        "hematocrit": [40, "%"],
        "wbc": [7e9, "L"],
        "fio2": [40, "%"],
        "pao2": [80, "mm Hg"],
        "gcs": 15,
        "sys_bp": [120, "mm Hg"],
        "dia_bp": [80, "mm Hg"],
        "temperature": [98.6, "degrees fahrenheit"],
    }


def test_apache_ii_zero_score():
    params = apache_base_params()
    result = apache_ii.apache_ii_explanation(params)
    assert result["Answer"] == 0


def test_apache_ii_organ_failure_false():
    params = apache_base_params()
    params["organ_failure_immunocompromise"] = False
    params["surgery_type"] = "Elective"
    result = apache_ii.apache_ii_explanation(params)
    assert result["Answer"] == 0


def test_apache_ii_aa_gradient_mid_range():
    params = apache_base_params()
    params["fio2"] = [60, "%"]
    params["a_a_gradient"] = 250
    result = apache_ii.apache_ii_explanation(params)
    assert result["Answer"] == 2


@pytest.mark.parametrize(
    "acute, chronic, creatinine, expected",
    [
        (True, False, 2.5, 6),
        (False, True, 2.5, 3),
        (True, False, 1.6, 4),
        (False, True, 1.6, 2),
        (False, False, 2.5, 3),
        (False, False, 1.6, 2),
    ],
)
def test_apache_ii_creatinine_branches(acute, chronic, creatinine, expected):
    params = apache_base_params()
    params["creatinine"] = [creatinine, "mg/dL"]
    if acute:
        params["acute_renal_failure"] = True
    if chronic:
        params["chronic_renal_failure"] = True
    result = apache_ii.apache_ii_explanation(params)
    assert result["Answer"] == expected


def test_psi_score_base():
    params = {
        "age": [40, "years"],
        "sex": "Male",
        "heart_rate": [80, "beats/min"],
        "temperature": [98.6, "degrees fahrenheit"],
        "pH": 7.4,
        "respiratory_rate": [16, "breaths/min"],
        "sys_bp": [120, "mm Hg"],
        "bun": [10, "mg/dL"],
        "sodium": [140, "mmol/L"],
        "glucose": [100, "mg/dL"],
        "hematocrit": [40, "%"],
        "partial_pressure_oxygen": [80, "mm Hg"],
    }
    result = psi_score.psi_score_explanation(params)
    assert result["Answer"] == 40


def test_psi_score_kpa_branch():
    params = {
        "age": [40, "years"],
        "sex": "Male",
        "heart_rate": [80, "beats/min"],
        "temperature": [98.6, "degrees fahrenheit"],
        "pH": 7.4,
        "respiratory_rate": [16, "breaths/min"],
        "sys_bp": [120, "mm Hg"],
        "bun": [10, "mg/dL"],
        "sodium": [140, "mmol/L"],
        "glucose": [100, "mg/dL"],
        "hematocrit": [40, "%"],
        "partial_pressure_oxygen": [7.9, "kPa"],
    }
    result = psi_score.psi_score_explanation(params)
    assert result["Answer"] == 50


def test_psi_score_kpa_no_points():
    params = {
        "age": [40, "years"],
        "sex": "Male",
        "heart_rate": [80, "beats/min"],
        "temperature": [98.6, "degrees fahrenheit"],
        "pH": 7.4,
        "respiratory_rate": [16, "breaths/min"],
        "sys_bp": [120, "mm Hg"],
        "bun": [10, "mg/dL"],
        "sodium": [140, "mmol/L"],
        "glucose": [100, "mg/dL"],
        "hematocrit": [40, "%"],
        "partial_pressure_oxygen": [8.0, "kPa"],
    }
    result = psi_score.psi_score_explanation(params)
    assert result["Answer"] == 40


def test_sofa_score_zero():
    params = {
        "pao2": [400, "mm Hg"],
        "fio2": [100, "%"],
        "platelet_count": [200000, "µL"],
        "bilirubin": [1.0, "mg/dL"],
        "creatinine": [1.0, "mg/dL"],
    }
    result = sofa.compute_sofa_explanation(params)
    assert result["Answer"] == 0


def test_sofa_explicit_false_support_map_low():
    params = {
        "pao2": [400, "mm Hg"],
        "fio2": [100, "%"],
        "platelet_count": [200000, "µL"],
        "bilirubin": [1.0, "mg/dL"],
        "creatinine": [1.0, "mg/dL"],
        "mechanical_ventilation": False,
        "cpap": False,
        "sys_bp": [90, "mm Hg"],
        "dia_bp": [50, "mm Hg"],
    }
    result = sofa.compute_sofa_explanation(params)
    assert result["Answer"] == 1


def test_sofa_hypotension_false():
    params = {
        "pao2": [400, "mm Hg"],
        "fio2": [100, "%"],
        "platelet_count": [200000, "µL"],
        "bilirubin": [1.0, "mg/dL"],
        "creatinine": [1.0, "mg/dL"],
        "mechanical_ventilation": False,
        "cpap": False,
        "sys_bp": [120, "mm Hg"],
        "dia_bp": [80, "mm Hg"],
        "hypotension": False,
    }
    result = sofa.compute_sofa_explanation(params)
    assert result["Answer"] == 0


def test_framingham_risk_score():
    params = {
        "age": [50, "years"],
        "sex": "Male",
        "total_cholesterol": [200, "mg/dL"],
        "hdl_cholesterol": [50, "mg/dL"],
        "sys_bp": [120, "mm Hg"],
        "smoker": False,
        "bp_medicine": False,
    }
    result = framingham_risk_score.framingham_risk_score_explanation(params)

    age = 50
    total_cholesterol = 200
    hdl = 50
    sys_bp = 120
    ln_age = math.log(age)
    ln_total = math.log(total_cholesterol)
    ln_hdl = math.log(hdl)
    ln_sys = math.log(sys_bp)
    ln_age_smoke = math.log(min(age, 70))

    beta = {
        "ln_age": 52.00961,
        "ln_total_cholesterol": 20.014077,
        "ln_hdl_cholesterol": -0.905964,
        "ln_sys_bp": 1.305784,
        "bp_medicine": 0.241549,
        "smoker": 12.096316,
        "ln_age_ln_total_cholesterol": -4.605038,
        "ln_age_smoker": -2.84367,
        "ln_age_ln_age": -2.93323,
        "constant": -172.300168,
    }

    risk_score = (
        beta["ln_age"] * ln_age
        + beta["ln_total_cholesterol"] * ln_total
        + beta["ln_hdl_cholesterol"] * ln_hdl
        + beta["ln_sys_bp"] * ln_sys
        + beta["bp_medicine"] * 0
        + beta["smoker"] * 0
        + beta["ln_age_ln_total_cholesterol"] * ln_age * ln_total
        + beta["ln_age_smoker"] * ln_age_smoke * 0
        + beta["ln_age_ln_age"] * ln_age * ln_age
        + beta["constant"]
    )
    risk_percentage = (1 - 0.9402 ** math.exp(risk_score)) * 100
    expected = round(risk_percentage, 3)

    assert result["Answer"] == expected


def test_framingham_risk_score_missing_flags():
    params = {
        "age": [50, "years"],
        "sex": "Male",
        "total_cholesterol": [200, "mg/dL"],
        "hdl_cholesterol": [50, "mg/dL"],
        "sys_bp": [120, "mm Hg"],
    }
    result = framingham_risk_score.framingham_risk_score_explanation(params)

    age = 50
    total_cholesterol = 200
    hdl = 50
    sys_bp = 120
    ln_age = math.log(age)
    ln_total = math.log(total_cholesterol)
    ln_hdl = math.log(hdl)
    ln_sys = math.log(sys_bp)
    ln_age_smoke = math.log(min(age, 70))

    beta = {
        "ln_age": 52.00961,
        "ln_total_cholesterol": 20.014077,
        "ln_hdl_cholesterol": -0.905964,
        "ln_sys_bp": 1.305784,
        "bp_medicine": 0.241549,
        "smoker": 12.096316,
        "ln_age_ln_total_cholesterol": -4.605038,
        "ln_age_smoker": -2.84367,
        "ln_age_ln_age": -2.93323,
        "constant": -172.300168,
    }

    risk_score = (
        beta["ln_age"] * ln_age
        + beta["ln_total_cholesterol"] * ln_total
        + beta["ln_hdl_cholesterol"] * ln_hdl
        + beta["ln_sys_bp"] * ln_sys
        + beta["bp_medicine"] * 0
        + beta["smoker"] * 0
        + beta["ln_age_ln_total_cholesterol"] * ln_age * ln_total
        + beta["ln_age_smoker"] * ln_age_smoke * 0
        + beta["ln_age_ln_age"] * ln_age * ln_age
        + beta["constant"]
    )
    risk_percentage = (1 - 0.9402 ** math.exp(risk_score)) * 100
    expected = round(risk_percentage, 3)

    assert result["Answer"] == expected


def test_framingham_risk_score_female():
    params = {
        "age": [50, "years"],
        "sex": "Female",
        "total_cholesterol": [200, "mg/dL"],
        "hdl_cholesterol": [50, "mg/dL"],
        "sys_bp": [120, "mm Hg"],
        "smoker": False,
        "bp_medicine": False,
    }
    result = framingham_risk_score.framingham_risk_score_explanation(params)

    age = 50
    total_cholesterol = 200
    hdl = 50
    sys_bp = 120
    ln_age = math.log(age)
    ln_total = math.log(total_cholesterol)
    ln_hdl = math.log(hdl)
    ln_sys = math.log(sys_bp)
    ln_age_smoke = math.log(min(age, 78))

    beta = {
        "ln_age": 31.764001,
        "ln_total_cholesterol": 22.465206,
        "ln_hdl_cholesterol": -1.187731,
        "ln_sys_bp": 2.552905,
        "bp_medicine": 0.420251,
        "smoker": 13.07543,
        "ln_age_ln_total_cholesterol": -5.060998,
        "ln_age_smoker": -2.996945,
        "constant": -146.5933061,
    }

    risk_score = (
        beta["ln_age"] * ln_age
        + beta["ln_total_cholesterol"] * ln_total
        + beta["ln_hdl_cholesterol"] * ln_hdl
        + beta["ln_sys_bp"] * ln_sys
        + beta["bp_medicine"] * 0
        + beta["smoker"] * 0
        + beta["ln_age_ln_total_cholesterol"] * ln_age * ln_total
        + beta["ln_age_smoker"] * ln_age_smoke * 0
        + beta["constant"]
    )
    risk_percentage = (1 - 0.98767 ** math.exp(risk_score)) * 100
    expected = round(risk_percentage, 3)

    assert result["Answer"] == expected
