from __future__ import annotations

import pytest

from rounding import round_number
import unit_converter_new as uc


@pytest.mark.parametrize(
    "value, src, tgt, expected",
    [
        (1, "L", "mL", 1000.0),
        (500, "mL", "L", 0.5),
        (2, "m^3", "L", 2000.0),
        (1000, "mm^3", "mL", 1.0),
        (10, "cm^3", "mL", 10.0),
    ],
)
def test_vol_to_vol_matrix(value, src, tgt, expected):
    _, result = uc.vol_to_vol_explanation(value, src, tgt)
    assert result == round_number(expected)


def test_vol_to_vol_conversion_factor():
    _, factor = uc.vol_to_vol_explanation(1, "L", "mL", conversion_factor=True)
    assert factor == round_number(1000)


def test_vol_to_vol_same_unit():
    _, result = uc.vol_to_vol_explanation(2, "mL", "mL")
    assert result == 2


@pytest.mark.parametrize(
    "value, src, tgt, expected",
    [
        (1000, "mg", "g", 1.0),
        (2, "mmol", "mol", 0.002),
        (3, "mol", "mmol", 3000.0),
    ],
)
def test_molg_to_molg(value, src, tgt, expected):
    _, result = uc.molg_to_molg_explanation(value, "compound", src, tgt)
    assert result == round_number(expected)


def test_mol_g_and_g_mol_roundtrip():
    _, mg = uc.mol_g_explanation(1, "glucose", 180.16, "mol", "mg")
    assert mg == round_number(180160)

    _, mol = uc.g_to_mol_explanation(180.16, "glucose", 180.16, "g", "mol")
    assert mol == 1.0


def test_meq_conversions():
    _, mmol = uc.mEq_to_mol_explanation(4, "sodium", 2, "mmol")
    assert mmol == 2.0

    _, meq = uc.mol_to_mEq_explanation(2, "sodium", 2, "mmol")
    assert meq == 4.0

    _, grams = uc.mEq_to_g_explanation(2, "sodium", 22.99, 1, "g")
    assert grams == round_number(0.04598)

    _, meq_from_g = uc.g_to_mEq_explanation(0.04598, "sodium", 22.99, 1, "g")
    assert meq_from_g == round_number(2.0)


def test_meq_to_mol_non_mmol_target():
    _, mol = uc.mEq_to_mol_explanation(4, "sodium", 2, "mol")
    assert mol == round_number(0.002)


def test_mol_to_meq_from_mol():
    _, meq = uc.mol_to_mEq_explanation(1, "sodium", 1, "mol")
    assert meq == round_number(1000)


def test_conversion_explanation_mass_volume():
    _, same = uc.conversion_explanation(100, "glucose", 180.16, None, "mg/dL", "mg/dL")
    assert same == 100

    _, converted = uc.conversion_explanation(100, "drug", 100, None, "mg/dL", "g/L")
    assert converted == round_number(1.0)

    _, mmol = uc.conversion_explanation(2, "sodium", 22.99, 1, "mEq/L", "mmol/L")
    assert mmol == 2.0


def test_conversion_explanation_same_mass_unit():
    _, converted = uc.conversion_explanation(5, "drug", 100, None, "mg/dL", "mg/L")
    assert converted == round_number(50.0)


def test_conversion_explanation_volume_only():
    _, converted = uc.conversion_explanation(2, "water", None, None, "L", "mL")
    assert converted == round_number(2000)


def test_conversion_explanation_volume_same_units():
    _, converted = uc.conversion_explanation(2, "water", None, None, "mL", "mL")
    assert converted == 2


def test_mass_conversion_branches():
    _, grams = uc.mass_conversion_explanation(1, "sodium", 1, 22.99, "mol", "g")
    assert grams == round_number(22.99)

    _, mol = uc.mass_conversion_explanation(22.99, "sodium", 1, 22.99, "g", "mol")
    assert mol == round_number(1.0)

    _, meq = uc.mass_conversion_explanation(1, "sodium", 1, 22.99, "mol", "mEq")
    assert meq == round_number(1000)

    _, grams_from_meq = uc.mass_conversion_explanation(10, "sodium", 1, 22.99, "mEq", "g")
    assert grams_from_meq == round_number(0.2299)

    _, meq_from_g = uc.mass_conversion_explanation(0.2299, "sodium", 1, 22.99, "g", "mEq")
    assert meq_from_g == round_number(10.0)


def test_units_per_liter_conversion():
    _, result = uc.convert_to_units_per_liter_explanation(5, "mm^3", "wbc", "L")
    assert result == round_number(5 * 1e6)


def test_invalid_units_raise():
    with pytest.raises(KeyError):
        uc.vol_to_vol_explanation(1, "invalid", "L")

    with pytest.raises(KeyError):
        uc.convert_to_units_per_liter_explanation(1, "invalid", "wbc", "L")
