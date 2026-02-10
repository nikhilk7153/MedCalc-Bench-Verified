from __future__ import annotations

import math

from rounding import round_number
import weight_conversion
import height_conversion
import age_conversion
import unit_converter_new
import convert_temperature


def test_round_number_behavior():
    assert round_number(0) == 0
    assert round_number(1.234567) == 1.23457
    assert round_number(0.0000854321) == 0.000085432
    assert round_number(-0.000012345) == -0.000012345
    assert round_number(0.000123456) == 0.00012


def test_weight_conversion_explanation():
    _, kg = weight_conversion.weight_conversion_explanation([100, "lbs"])
    assert kg == round_number(100 * 0.453592)

    _, kg_from_g = weight_conversion.weight_conversion_explanation([1000, "g"])
    assert kg_from_g == 1.0

    _, kg_same = weight_conversion.weight_conversion_explanation([70, "kg"])
    assert kg_same == 70


def test_height_conversion_explanation():
    _, meters = height_conversion.height_conversion_explanation([5, "ft", 8, "in"])
    assert meters == round_number((5 * 12 + 8) * 0.0254)

    _, meters_from_cm = height_conversion.height_conversion_explanation([180, "cm"])
    assert meters_from_cm == round_number(1.8)

    _, meters_from_in = height_conversion.height_conversion_explanation([70, "in"])
    assert meters_from_in == round_number(70 * 0.0254)

    _, meters_from_m = height_conversion.height_conversion_explanation([1.7, "m"])
    assert meters_from_m == 1.7

    _, meters_from_ft = height_conversion.height_conversion_explanation([6, "ft"])
    assert meters_from_ft == round_number(6 * 0.3048)


def test_height_conversion_cm_and_in():
    _, cm = height_conversion.height_conversion_explanation_cm([5, "ft", 8, "in"])
    assert cm == round_number((5 * 12 + 8) * 2.54)

    _, cm_from_ft = height_conversion.height_conversion_explanation_cm([5, "ft"])
    assert cm_from_ft == round_number(5 * 30.48)

    _, inches = height_conversion.height_conversion_explanation_in([1.8, "m"])
    assert inches == round_number(1.8 * 39.3701)

    _, inches_from_cm = height_conversion.height_conversion_explanation_in([180, "cm"])
    assert inches_from_cm == round_number(180 * 0.393701)

    _, cm_from_m = height_conversion.height_conversion_explanation_cm([1.7, "m"])
    assert cm_from_m == round_number(170)

    _, cm_from_in = height_conversion.height_conversion_explanation_cm([70, "in"])
    assert cm_from_in == round_number(70 * 2.54)

    _, inches_from_ft = height_conversion.height_conversion_explanation_in([6, "ft"])
    assert inches_from_ft == round_number(72)

    _, inches_from_in = height_conversion.height_conversion_explanation_in([70, "in"])
    assert inches_from_in == 70

    _, inches_from_tuple = height_conversion.height_conversion_explanation_in([5, "ft", 8, "in"])
    assert inches_from_tuple == round_number(68)


def test_age_conversion():
    assert age_conversion.age_conversion([30, "years"]) == 30
    assert age_conversion.age_conversion([18, "months"]) == 1
    assert age_conversion.age_conversion([30, "months"]) == 2
    assert age_conversion.age_conversion([26, "weeks"]) == 0
    assert age_conversion.age_conversion([10, "days"]) == 0
    assert age_conversion.age_conversion([1, "decades", 20, "years"]) == 20

    text, years = age_conversion.age_conversion_explanation([18, "months"])
    assert years == 1
    assert "year" in text


def test_age_conversion_explanation_multiple_parts():
    text, years = age_conversion.age_conversion_explanation([1, "years", 6, "months", 10, "days"])
    assert years == 1
    assert ", and " in text


def test_age_conversion_explanation_no_year():
    text, years = age_conversion.age_conversion_explanation([6, "months", 15, "days"])
    assert years == 0
    assert "0 years old" in text


def test_unit_converters_basic():
    _, ml = unit_converter_new.vol_to_vol_explanation(2, "L", "mL")
    assert ml == round_number(2000)

    _, grams = unit_converter_new.molg_to_molg_explanation(1000, "drug", "mg", "g")
    assert grams == 1.0

    _, mol = unit_converter_new.g_to_mol_explanation(180.16, "glucose", 180.16, "g", "mol")
    assert mol == 1.0

    _, mmol = unit_converter_new.mEq_to_mol_explanation(2, "sodium", 2, "mmol")
    assert mmol == 1.0

    _, meq = unit_converter_new.mol_to_mEq_explanation(2, "sodium", 2, "mmol")
    assert meq == 4.0


def test_conversion_explanation_and_pressure():
    _, same = unit_converter_new.conversion_explanation(100, "glucose", 180.16, None, "mg/dL", "mg/dL")
    assert same == 100

    _, grams = unit_converter_new.conversion_explanation(500, "drug", 100, None, "mg", "g")
    assert grams == round_number(0.5)

    _, kpa = unit_converter_new.mmHg_to_kPa_explanation(100, "oxygen")
    assert kpa == round_number(13.3322)

    _, mmhg = unit_converter_new.kPa_to_mmHg_explanation(13.3322, "oxygen")
    assert mmhg == round_number(13.3322 * 7.50062)

    _, count_per_l = unit_converter_new.convert_to_units_per_liter_explanation(5, "mL", "wbc", "L")
    assert count_per_l == round_number(5000)


def test_temperature_conversion():
    _, celsius = convert_temperature.fahrenheit_to_celsius_explanation(98.6, "degrees fahrenheit")
    assert celsius == round_number(37.0)

    _, same = convert_temperature.fahrenheit_to_celsius_explanation(37, "degrees celsius")
    assert same == 37
