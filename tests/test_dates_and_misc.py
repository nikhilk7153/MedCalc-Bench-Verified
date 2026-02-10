from __future__ import annotations

from datetime import datetime, timedelta

import pytest

from rounding import round_number
import estimated_due_date
import estimated_conception_date
import estimated_gestational_age
import steroid_conversion_calculator
import mme


def test_estimated_due_date_cycle_adjustment():
    params = {"menstrual_date": "01/01/2024", "cycle_length": 30}
    result = estimated_due_date.add_40_weeks_explanation(params)
    expected_date = datetime.strptime("01/01/2024", "%m/%d/%Y") + timedelta(weeks=40, days=2)
    assert result["Answer"] == expected_date.strftime("%m/%d/%Y")


def test_estimated_due_date_short_cycle():
    params = {"menstrual_date": "01/01/2024", "cycle_length": 26}
    result = estimated_due_date.add_40_weeks_explanation(params)
    expected_date = datetime.strptime("01/01/2024", "%m/%d/%Y") + timedelta(weeks=40, days=-2)
    assert result["Answer"] == expected_date.strftime("%m/%d/%Y")


def test_estimated_due_date_standard_cycle():
    params = {"menstrual_date": "01/01/2024", "cycle_length": 28}
    result = estimated_due_date.add_40_weeks_explanation(params)
    expected_date = datetime.strptime("01/01/2024", "%m/%d/%Y") + timedelta(weeks=40)
    assert result["Answer"] == expected_date.strftime("%m/%d/%Y")


def test_estimated_conception_date():
    params = {"menstrual_date": "03/15/2024"}
    result = estimated_conception_date.add_2_weeks_explanation(params)
    expected = datetime.strptime("03/15/2024", "%m/%d/%Y") + timedelta(weeks=2)
    assert result["Answer"] == expected.strftime("%m/%d/%Y")


def test_estimated_gestational_age():
    params = {"menstrual_date": "01/01/2024", "current_date": "02/13/2024"}
    result = estimated_gestational_age.compute_gestational_age_explanation(params)
    delta = datetime.strptime("02/13/2024", "%m/%d/%Y") - datetime.strptime("01/01/2024", "%m/%d/%Y")
    weeks = delta.days // 7
    days = delta.days % 7
    assert result["Answer"] == (f"{weeks} weeks", f"{days} days")


def test_estimated_gestational_age_reverse_dates():
    params = {"menstrual_date": "02/12/2024", "current_date": "01/01/2024"}
    result = estimated_gestational_age.compute_gestational_age_explanation(params)
    delta = datetime.strptime("02/12/2024", "%m/%d/%Y") - datetime.strptime("01/01/2024", "%m/%d/%Y")
    weeks = delta.days // 7
    days = delta.days % 7
    assert result["Answer"] == (f"{weeks} weeks", f"{days} days")


def test_estimated_gestational_age_days_only():
    params = {"menstrual_date": "01/01/2024", "current_date": "01/06/2024"}
    result = estimated_gestational_age.compute_gestational_age_explanation(params)
    assert result["Answer"] == ("0 weeks", "5 days")


def test_estimated_gestational_age_weeks_only():
    params = {"menstrual_date": "01/01/2024", "current_date": "01/15/2024"}
    result = estimated_gestational_age.compute_gestational_age_explanation(params)
    assert result["Answer"] == ("2 weeks", "0 days")


def test_steroid_conversion():
    params = {
        "input steroid": ["PredniSONE PO", 10, "mg"],
        "target steroid": "Hydrocortisone IV",
    }
    result = steroid_conversion_calculator.compute_steroid_conversion_explanation(params)
    conversion_factor = round_number(26.67 / 6.67)
    expected = round_number(10 * conversion_factor)
    assert result["Answer"] == pytest.approx(expected, abs=1e-4)


def test_mme_single_drug():
    params = {
        "Codeine Dose": [30, "mg"],
        "Codeine Dose Per Day": [2, "per day"],
    }
    result = mme.mme_explanation(params)
    expected = round_number(30 * 2 * 0.15)
    assert result["Answer"] == expected
