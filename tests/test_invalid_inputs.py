from __future__ import annotations

import pytest

import age_conversion
import framingham_risk_score
import mdrd_gfr
import qt_calculator_bazett


def _mdrd_fn():
    return getattr(mdrd_gfr, "mdrd_gfr_explanation", mdrd_gfr.mrdr_gfr_explanation)


def test_age_conversion_invalid_length():
    with pytest.raises(IndexError):
        age_conversion.age_conversion([5])


def test_framingham_invalid_age_raises():
    params = {
        "age": [0, "years"],
        "sex": "Male",
        "total_cholesterol": [200, "mg/dL"],
        "hdl_cholesterol": [50, "mg/dL"],
        "sys_bp": [120, "mm Hg"],
        "smoker": False,
        "bp_medicine": False,
    }
    with pytest.raises(ValueError):
        framingham_risk_score.framingham_risk_score_explanation(params)


def test_mdrd_invalid_age_raises():
    params = {
        "sex": "Male",
        "age": [0, "years"],
        "creatinine": [1.0, "mg/dL"],
    }
    with pytest.raises(ValueError):
        _mdrd_fn()(params)


def test_qt_bazett_divide_by_zero():
    params = {"heart_rate": [0, "beats per minute"], "qt_interval": [400, "msec"]}
    with pytest.raises(ZeroDivisionError):
        qt_calculator_bazett.bazett_calculator_explanation(params)
