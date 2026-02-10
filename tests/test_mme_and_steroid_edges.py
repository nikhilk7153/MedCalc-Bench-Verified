from __future__ import annotations

import pytest
from rounding import round_number
import mme
import steroid_conversion_calculator


def test_mme_multiple_drugs_accumulates():
    params = {
        "Codeine Dose": [30, "mg"],
        "Codeine Dose Per Day": [2, "per day"],
        "OxyCODONE Dose": [10, "mg"],
        "OxyCODONE Dose Per Day": [3, "per day"],
    }
    result = mme.mme_explanation(params)
    expected = round_number(30 * 2 * 0.15 + 10 * 3 * 1.5)
    assert result["Answer"] == expected


def test_mme_fentanyl_buccal_micrograms():
    params = {
        "FentaNYL buccal Dose": [100, "µg"],
        "FentaNYL buccal Dose Per Day": [2, "per day"],
    }
    with pytest.raises(ValueError):
        mme.mme_explanation(params)


def test_mme_fentanyl_buccal_mg_conversion():
    params = {
        "FentaNYL buccal Dose": [0.1, "mg"],
        "FentaNYL buccal Dose Per Day": [2, "per day"],
    }
    with pytest.raises(ValueError):
        mme.mme_explanation(params)


def test_mme_fentanyl_patch_micrograms():
    params = {
        "FentANYL patch Dose": [25, "µg"],
        "FentANYL patch Dose Per Day": [1, "per day"],
    }
    result = mme.mme_explanation(params)
    expected = round_number(25 * 1 * 2.4)
    assert result["Answer"] == expected


def test_steroid_conversion_micrograms_input():
    params = {
        "input steroid": ["Dexamethasone PO", 750, "µg"],
        "target steroid": "PredniSONE PO",
    }
    result = steroid_conversion_calculator.compute_steroid_conversion_explanation(params)
    conversion_factor = round_number(6.67 / 1.0)
    expected = round_number(0.75 * conversion_factor)
    assert result["Answer"] == expected


def test_steroid_conversion_methylpred_iv():
    params = {
        "input steroid": ["MethylPrednisoLONE IV", 4, "mg"],
        "target steroid": "PredniSONE PO",
    }
    result = steroid_conversion_calculator.compute_steroid_conversion_explanation(params)
    conversion_factor = round_number(6.67 / 5.33)
    expected = round_number(4 * conversion_factor)
    assert result["Answer"] == pytest.approx(expected, abs=1e-4)


def test_steroid_conversion_wrapper():
    params = {
        "input steroid": ["PredniSONE PO", 10, "mg"],
        "target steroid": "Hydrocortisone IV",
    }
    expected = steroid_conversion_calculator.compute_steroid_conversion_explanation(params)["Answer"]
    assert steroid_conversion_calculator.compute_steroid_conversion(params) == expected
