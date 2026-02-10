from __future__ import annotations

import pytest
from rounding import round_number
import qt_calculator_bazett
import qt_calculator_fredericia
import qt_calculator_framingham
import qt_calculator_hodges
import qt_calculator_rautaharju


def test_qt_calculators_consistency():
    params = {"heart_rate": [60, "beats per minute"], "qt_interval": [400, "msec"]}

    assert qt_calculator_bazett.bazett_calculator_explanation(params)["Answer"] == 400
    assert qt_calculator_fredericia.fredericia_calculator_explanation(params)["Answer"] == 400
    assert qt_calculator_framingham.framingham_calculator_explanation(params)["Answer"] == 400
    assert qt_calculator_hodges.hodges_calculator_explanation(params)["Answer"] == 400
    assert qt_calculator_rautaharju.rautaharju_calculator_explanation(params)["Answer"] == 400


def test_qt_bazett_nonstandard_hr():
    params = {"heart_rate": [75, "beats per minute"], "qt_interval": [400, "msec"]}
    rr_interval = round_number(60 / 75)
    expected = round_number(400 / (rr_interval ** 0.5))
    assert qt_calculator_bazett.bazett_calculator_explanation(params)["Answer"] == pytest.approx(expected, abs=1e-3)


def test_qt_bazett_rr_rounding():
    params = {"heart_rate": [73, "beats per minute"], "qt_interval": [400, "msec"]}
    rr_interval = round_number(60 / 73)
    expected = round_number(400 / (rr_interval ** 0.5))
    assert qt_calculator_bazett.bazett_calculator_explanation(params)["Answer"] == pytest.approx(expected, abs=1e-3)


def test_qt_fredericia_nonstandard_hr():
    params = {"heart_rate": [75, "beats per minute"], "qt_interval": [400, "msec"]}
    rr_interval = round_number(60 / 75)
    expected = round_number(400 / (rr_interval ** (1 / 3)))
    assert qt_calculator_fredericia.fredericia_calculator_explanation(params)["Answer"] == pytest.approx(expected, abs=1e-3)


def test_qt_fredericia_rr_rounding():
    params = {"heart_rate": [73, "beats per minute"], "qt_interval": [400, "msec"]}
    rr_interval = round_number(60 / 73)
    expected = round_number(400 / (rr_interval ** (1 / 3)))
    assert qt_calculator_fredericia.fredericia_calculator_explanation(params)["Answer"] == pytest.approx(expected, abs=1e-3)


def test_qt_framingham_nonstandard_hr():
    params = {"heart_rate": [75, "beats per minute"], "qt_interval": [400, "msec"]}
    rr_interval = round_number(60 / 75)
    expected = round_number(400 + (154 * (1 - rr_interval)))
    assert qt_calculator_framingham.framingham_calculator_explanation(params)["Answer"] == pytest.approx(expected, abs=1e-3)


def test_qt_framingham_rr_rounding():
    params = {"heart_rate": [73, "beats per minute"], "qt_interval": [400, "msec"]}
    rr_interval = round_number(60 / 73)
    expected = round_number(400 + (154 * (1 - rr_interval)))
    assert qt_calculator_framingham.framingham_calculator_explanation(params)["Answer"] == pytest.approx(expected, abs=1e-3)


def test_qt_hodges_nonstandard_hr():
    params = {"heart_rate": [75, "beats per minute"], "qt_interval": [400, "msec"]}
    rr_interval = round_number(60 / 75)
    expected = round_number(400 + 1.75 * ((60 / rr_interval) - 60))
    assert qt_calculator_hodges.hodges_calculator_explanation(params)["Answer"] == pytest.approx(expected, abs=1e-3)


def test_qt_hodges_rr_rounding():
    params = {"heart_rate": [73, "beats per minute"], "qt_interval": [400, "msec"]}
    rr_interval = round_number(60 / 73)
    expected = round_number(400 + 1.75 * ((60 / rr_interval) - 60))
    assert qt_calculator_hodges.hodges_calculator_explanation(params)["Answer"] == pytest.approx(expected, abs=1e-3)


def test_qt_rautaharju_nonstandard_hr():
    params = {"heart_rate": [75, "beats per minute"], "qt_interval": [400, "msec"]}
    expected = round_number(400 * (120 + 75) / 180)
    assert qt_calculator_rautaharju.rautaharju_calculator_explanation(params)["Answer"] == expected


def test_qt_rautaharju_nonstandard_hr_rounding():
    params = {"heart_rate": [73, "beats per minute"], "qt_interval": [400, "msec"]}
    expected = round_number(400 * (120 + 73) / 180)
    assert qt_calculator_rautaharju.rautaharju_calculator_explanation(params)["Answer"] == expected
