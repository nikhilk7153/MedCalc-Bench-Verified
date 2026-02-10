from __future__ import annotations

import math

from rounding import round_number
import meldna
import creatinine_clearance


def compute_meldna_expected(
    creatinine,
    bilirubin,
    inr,
    sodium,
    albumin,
    age,
    sex=None,
    dialysis_twice=False,
    cvvhd=False,
):
    if dialysis_twice or cvvhd:
        creatinine = 3.0
    elif creatinine < 1.0:
        creatinine = 1.0
    elif creatinine > 3.0:
        creatinine = 3.0

    if bilirubin < 1.0:
        bilirubin = 1.0

    if inr < 1.0:
        inr = 1.0

    if sodium < 125:
        sodium = 125
    elif sodium > 137:
        sodium = 137

    if albumin < 1.5:
        albumin = 1.5
    elif albumin > 3.5:
        albumin = 3.5

    ln_bilirubin = math.log(bilirubin)
    ln_inr = math.log(inr)
    ln_creatinine = math.log(creatinine)
    sodium_term = 137 - sodium
    albumin_term = 3.5 - albumin

    base_meld = (
        4.56 * ln_bilirubin
        + 0.82 * sodium_term
        - 0.24 * sodium_term * ln_bilirubin
        + 9.09 * ln_inr
        + 11.14 * ln_creatinine
        + 1.85 * albumin_term
        - 1.83 * albumin_term * ln_creatinine
    )

    if age >= 18:
        female = 1 if sex == "Female" else 0
        meld_raw = 1.33 * female + base_meld + 6
    else:
        meld_raw = base_meld + 7.33

    meld = round(meld_raw)
    if meld < 6:
        return 6
    if meld > 40:
        return 40
    return meld


def test_meldna_high_values_caps_at_40():
    params = {
        "creatinine": [3.0, "mg/dL"],
        "bilirubin": [20.0, "mg/dL"],
        "inr": 5.0,
        "sodium": [130, "mEq/L"],
        "albumin": [2.0, "g/dL"],
        "age": [45, "years"],
        "sex": "Female",
    }
    result = meldna.compute_meldna_explanation(params)
    expected = compute_meldna_expected(3.0, 20.0, 5.0, 130, 2.0, 45, "Female")
    assert expected == 40
    assert result["Answer"] == expected == 40


def test_meldna_dialysis_override_creatinine():
    params = {
        "creatinine": [0.5, "mg/dL"],
        "bilirubin": [1.5, "mg/dL"],
        "inr": 1.2,
        "sodium": [136, "mEq/L"],
        "albumin": [3.0, "g/dL"],
        "age": [40, "years"],
        "sex": "Male",
        "dialysis_twice": True,
    }
    result = meldna.compute_meldna_explanation(params)
    expected = compute_meldna_expected(
        0.5, 1.5, 1.2, 136, 3.0, 40, "Male", dialysis_twice=True
    )
    assert result["Answer"] == expected


def test_meldna_cvvhd_override_creatinine():
    params = {
        "creatinine": [0.5, "mg/dL"],
        "bilirubin": [1.5, "mg/dL"],
        "inr": 1.2,
        "sodium": [136, "mEq/L"],
        "albumin": [3.0, "g/dL"],
        "age": [40, "years"],
        "sex": "Male",
        "cvvhd": True,
    }
    result = meldna.compute_meldna_explanation(params)
    expected = compute_meldna_expected(
        0.5, 1.5, 1.2, 136, 3.0, 40, "Male", cvvhd=True
    )
    assert result["Answer"] == expected


def test_meldna_explicit_no_dialysis():
    params = {
        "creatinine": [1.2, "mg/dL"],
        "bilirubin": [1.5, "mg/dL"],
        "inr": 1.2,
        "sodium": [136, "mEq/L"],
        "albumin": [3.0, "g/dL"],
        "age": [40, "years"],
        "sex": "Male",
        "dialysis_twice": False,
        "cvvhd": False,
    }
    result = meldna.compute_meldna_explanation(params)
    expected = compute_meldna_expected(1.2, 1.5, 1.2, 136, 3.0, 40, "Male")
    assert result["Answer"] == expected


def test_meldna_sodium_high_capped():
    params = {
        "creatinine": [1.2, "mg/dL"],
        "bilirubin": [1.5, "mg/dL"],
        "inr": 1.2,
        "sodium": [150, "mEq/L"],
        "albumin": [3.0, "g/dL"],
        "age": [40, "years"],
        "sex": "Male",
    }
    result = meldna.compute_meldna_explanation(params)
    expected = compute_meldna_expected(1.2, 1.5, 1.2, 150, 3.0, 40, "Male")
    assert result["Answer"] == expected


def test_meldna_sodium_low_capped():
    params = {
        "creatinine": [1.2, "mg/dL"],
        "bilirubin": [1.5, "mg/dL"],
        "inr": 1.2,
        "sodium": [120, "mEq/L"],
        "albumin": [3.0, "g/dL"],
        "age": [40, "years"],
        "sex": "Male",
    }
    result = meldna.compute_meldna_explanation(params)
    expected = compute_meldna_expected(1.2, 1.5, 1.2, 120, 3.0, 40, "Male")
    assert result["Answer"] == expected


def test_meldna_albumin_low_capped():
    params = {
        "creatinine": [1.2, "mg/dL"],
        "bilirubin": [1.5, "mg/dL"],
        "inr": 1.2,
        "sodium": [136, "mEq/L"],
        "albumin": [1.0, "g/dL"],
        "age": [40, "years"],
        "sex": "Male",
    }
    result = meldna.compute_meldna_explanation(params)
    expected = compute_meldna_expected(1.2, 1.5, 1.2, 136, 1.0, 40, "Male")
    assert result["Answer"] == expected


def test_meldna_albumin_high_capped():
    params = {
        "creatinine": [1.2, "mg/dL"],
        "bilirubin": [1.5, "mg/dL"],
        "inr": 1.2,
        "sodium": [136, "mEq/L"],
        "albumin": [4.0, "g/dL"],
        "age": [40, "years"],
        "sex": "Male",
    }
    result = meldna.compute_meldna_explanation(params)
    expected = compute_meldna_expected(1.2, 1.5, 1.2, 136, 4.0, 40, "Male")
    assert result["Answer"] == expected


def test_meldna_creatinine_min_capped():
    params = {
        "creatinine": [0.5, "mg/dL"],
        "bilirubin": [1.5, "mg/dL"],
        "inr": 1.2,
        "sodium": [136, "mEq/L"],
        "albumin": [3.0, "g/dL"],
        "age": [40, "years"],
        "sex": "Male",
    }
    result = meldna.compute_meldna_explanation(params)
    expected = compute_meldna_expected(0.5, 1.5, 1.2, 136, 3.0, 40, "Male")
    assert result["Answer"] == expected


def test_meldna_creatinine_max_capped():
    params = {
        "creatinine": [5.0, "mg/dL"],
        "bilirubin": [1.5, "mg/dL"],
        "inr": 1.2,
        "sodium": [136, "mEq/L"],
        "albumin": [3.0, "g/dL"],
        "age": [40, "years"],
        "sex": "Male",
    }
    result = meldna.compute_meldna_explanation(params)
    expected = compute_meldna_expected(5.0, 1.5, 1.2, 136, 3.0, 40, "Male")
    assert result["Answer"] == expected


def test_meldna_rounding_midrange():
    params = {
        "creatinine": [1.2, "mg/dL"],
        "bilirubin": [1.7, "mg/dL"],
        "inr": 1.3,
        "sodium": [135, "mEq/L"],
        "albumin": [3.2, "g/dL"],
        "age": [50, "years"],
        "sex": "Male",
    }
    result = meldna.compute_meldna_explanation(params)
    expected = compute_meldna_expected(1.2, 1.7, 1.3, 135, 3.2, 50, "Male")
    assert expected == 15
    assert result["Answer"] == expected


def test_meldna_adolescent_formula():
    params = {
        "creatinine": [1.2, "mg/dL"],
        "bilirubin": [1.7, "mg/dL"],
        "inr": 1.3,
        "sodium": [135, "mEq/L"],
        "albumin": [3.2, "g/dL"],
        "age": [16, "years"],
    }
    result = meldna.compute_meldna_explanation(params)
    expected = compute_meldna_expected(1.2, 1.7, 1.3, 135, 3.2, 16)
    assert expected == 16
    assert result["Answer"] == expected


def test_meldna_age_missing_defaults_adult():
    params = {
        "creatinine": [1.2, "mg/dL"],
        "bilirubin": [1.5, "mg/dL"],
        "inr": 1.2,
        "sodium": [136, "mEq/L"],
        "albumin": [3.0, "g/dL"],
    }
    result = meldna.compute_meldna_explanation(params)
    expected = compute_meldna_expected(1.2, 1.5, 1.2, 136, 3.0, 18)
    assert result["Answer"] == expected


def test_meldna_under_12_note():
    params = {
        "creatinine": [1.2, "mg/dL"],
        "bilirubin": [1.5, "mg/dL"],
        "inr": 1.2,
        "sodium": [136, "mEq/L"],
        "albumin": [3.0, "g/dL"],
        "age": [10, "years"],
    }
    result = meldna.compute_meldna_explanation(params)
    expected = compute_meldna_expected(1.2, 1.5, 1.2, 136, 3.0, 10)
    assert result["Answer"] == expected


def test_meldna_score_floor():
    params = {
        "creatinine": [1.0, "mg/dL"],
        "bilirubin": [1.0, "mg/dL"],
        "inr": 1.0,
        "sodium": [137, "mEq/L"],
        "albumin": [3.5, "g/dL"],
        "age": [18, "years"],
    }
    result = meldna.compute_meldna_explanation(params)
    assert result["Answer"] == 6


def _expected_crcl(age, adjusted_weight, creatinine, sex):
    constant = 1.0 if sex == "Male" else 0.85
    return round_number(((140 - age) * adjusted_weight * constant) / (creatinine * 72))


def _ibw(height_m, sex):
    height_in = round_number(height_m * 39.3701)
    base = 50.0 if sex == "Male" else 45.5
    return round_number(base + 2.3 * (height_in - 60))


def _abw(weight_kg, ibw):
    return round_number(ibw + 0.4 * (weight_kg - ibw))


def test_creatinine_clearance_underweight_branch():
    params = {
        "weight": [45, "kg"],
        "height": [1.7, "m"],
        "sex": "Male",
        "age": [40, "years"],
        "creatinine": [1.0, "mg/dL"],
    }
    result = creatinine_clearance.generate_cockcroft_gault_explanation(params)
    expected = _expected_crcl(40, 45, 1.0, "Male")
    assert result["Answer"] == expected


def test_creatinine_clearance_normal_weight_branch():
    params = {
        "weight": [68, "kg"],
        "height": [1.7, "m"],
        "sex": "Male",
        "age": [40, "years"],
        "creatinine": [1.0, "mg/dL"],
    }
    result = creatinine_clearance.generate_cockcroft_gault_explanation(params)
    ibw = _ibw(1.7, "Male")
    adjusted = min(ibw, 68)
    expected = _expected_crcl(40, adjusted, 1.0, "Male")
    assert result["Answer"] == expected


def test_creatinine_clearance_overweight_female_branch():
    params = {
        "weight": [100, "kg"],
        "height": [1.7, "m"],
        "sex": "Female",
        "age": [30, "years"],
        "creatinine": [1.2, "mg/dL"],
    }
    result = creatinine_clearance.generate_cockcroft_gault_explanation(params)
    ibw = _ibw(1.7, "Female")
    adjusted = _abw(100, ibw)
    expected = _expected_crcl(30, adjusted, 1.2, "Female")
    assert result["Answer"] == expected
