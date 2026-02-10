from __future__ import annotations

from rounding import round_number
import bmi_calculator
import bsa_calculator
import ideal_body_weight
import adjusted_body_weight
import target_weight
import maintenance_fluid_calc
import mean_arterial_pressure


def test_bmi_calculator():
    params = {
        "height": [5, "ft", 8, "in"],
        "weight": [150, "lbs"],
    }
    result = bmi_calculator.bmi_calculator_explanation(params)
    height_m = round_number((5 * 12 + 8) * 0.0254)
    weight_kg = round_number(150 * 0.453592)
    expected = round_number(weight_kg / (height_m * height_m))
    assert result["Answer"] == expected


def test_bsa_calculator():
    params = {
        "height": [170, "cm"],
        "weight": [70, "kg"],
    }
    result = bsa_calculator.bsa_calculator_explaination(params)
    expected = round_number(((70 * 170) / 3600) ** 0.5)
    assert result["Answer"] == expected


def test_ideal_body_weight():
    params = {
        "height": [70, "in"],
        "sex": "Male",
    }
    result = ideal_body_weight.ibw_explanation(params)
    expected = round_number(50 + 2.3 * (70 - 60))
    assert result["Answer"] == expected


def test_adjusted_body_weight():
    params = {
        "height": [70, "in"],
        "sex": "Male",
        "weight": [200, "lbs"],
    }
    result = adjusted_body_weight.abw_explanation(params)
    ibw = round_number(50 + 2.3 * (70 - 60))
    weight_kg = round_number(200 * 0.453592)
    expected = round_number(ibw + 0.4 * (weight_kg - ibw))
    assert result["Answer"] == expected


def test_target_weight():
    params = {
        "body_mass_index": [25, "kg/m^2"],
        "height": [1.7, "m"],
    }
    result = target_weight.targetweight_explanation(params)
    expected = round_number(25 * (1.7 * 1.7))
    assert result["Answer"] == expected


def test_maintenance_fluid_calc_branches():
    low = maintenance_fluid_calc.maintenance_fluid_explanation({"weight": [8, "kg"]})
    assert low["Answer"] == round_number(32)

    mid = maintenance_fluid_calc.maintenance_fluid_explanation({"weight": [15, "kg"]})
    assert mid["Answer"] == round_number(40 + 2 * (15 - 10))

    high = maintenance_fluid_calc.maintenance_fluid_explanation({"weight": [25, "kg"]})
    assert high["Answer"] == round_number(60 + (25 - 20))


def test_maintenance_fluid_calc_boundaries():
    at_ten = maintenance_fluid_calc.maintenance_fluid_explanation({"weight": [10, "kg"]})
    assert at_ten["Answer"] == round_number(40)

    at_twenty = maintenance_fluid_calc.maintenance_fluid_explanation({"weight": [20, "kg"]})
    assert at_twenty["Answer"] == round_number(60)


def test_mean_arterial_pressure():
    params = {"sys_bp": [120, "mm Hg"], "dia_bp": [80, "mm Hg"]}
    result = mean_arterial_pressure.mean_arterial_pressure_explanation(params)
    expected = round_number(120 / 3 + 2 * 80 / 3)
    assert result["Answer"] == expected
