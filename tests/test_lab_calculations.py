from __future__ import annotations

import importlib.util
import math
from pathlib import Path

from rounding import round_number
import anion_gap
import albumin_corrected_anion
import delta_gap
import delta_ratio
import albumin_corrected_delta_gap
import albumin_delta_ratio
import sOsm
import sodium_correction_hyperglycemia
import free_water_deficit
import calcium_correction
import ldl_calculated
import unit_converter_new
import homa_ir
import compute_fena
import creatinine_clearance
import mdrd_gfr
import meldna
import fibrosis_4


def _load_ckd_epi_module():
    root = Path(__file__).resolve().parents[1]
    path = root / "calculator_implementations" / "ckd-epi_2021_creatinine.py"
    spec = importlib.util.spec_from_file_location("ckd_epi_2021_creatinine", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)  # type: ignore[arg-type]
    return module


def _mdrd_fn():
    # Compatibility: some revisions export mrdr_gfr_explanation.
    return getattr(mdrd_gfr, "mdrd_gfr_explanation", mdrd_gfr.mrdr_gfr_explanation)


def base_electrolytes():
    return {
        "sodium": [140, "mEq/L"],
        "chloride": [100, "mEq/L"],
        "bicarbonate": [20, "mEq/L"],
        "albumin": [3.0, "g/dL"],
    }


def test_anion_gap_and_albumin_corrections():
    params = base_electrolytes()
    anion = anion_gap.compute_anion_gap_explanation(params)
    assert anion["Answer"] == round_number(140 - (100 + 20))

    corrected = albumin_corrected_anion.compute_albumin_corrected_anion_explanation(params)
    expected_corrected = round_number(20 + 2.5 * (4 - 3.0))
    assert corrected["Answer"] == expected_corrected

    dg = delta_gap.compute_delta_gap_explanation(params)
    assert dg["Answer"] == round_number(20 - 12)

    acdg = albumin_corrected_delta_gap.compute_albumin_corrected_delta_gap_explanation(params)
    assert acdg["Answer"] == round_number(expected_corrected - 12)

    dr = delta_ratio.compute_delta_ratio_explanation(params)
    assert dr["Answer"] == round_number(8 / (24 - 20))

    adr = albumin_delta_ratio.compute_albumin_delta_ratio_explanation(params)
    assert adr["Answer"] == round_number(acdg["Answer"] / (24 - 20))


def test_delta_ratio_bicarbonate_mmol_per_l():
    params = base_electrolytes()
    params["bicarbonate"] = [20, "mmol/L"]
    dr = delta_ratio.compute_delta_ratio_explanation(params)
    assert dr["Answer"] == round_number(8 / (24 - 20))


def test_albumin_corrected_anion_albumin_g_per_l():
    params = base_electrolytes()
    params["albumin"] = [30.0, "g/L"]
    corrected = albumin_corrected_anion.compute_albumin_corrected_anion_explanation(params)
    albumin = unit_converter_new.conversion_explanation(30.0, "albumin", None, None, "g/L", "g/dL")[1]
    expected = round_number(20 + 2.5 * (4 - albumin))
    assert corrected["Answer"] == expected


def test_serum_osmolality():
    params = {
        "sodium": [140, "mmol/L"],
        "bun": [14, "mg/dL"],
        "glucose": [90, "mg/dL"],
    }
    result = sOsm.compute_serum_osmolality_explanation(params)
    assert result["Answer"] == round_number(2 * 140 + 14 / 2.8 + 90 / 18)


def test_serum_osmolality_bun_mmol_per_l():
    params = {
        "sodium": [140, "mmol/L"],
        "bun": [7.0, "mmol/L"],
        "glucose": [90, "mg/dL"],
    }
    result = sOsm.compute_serum_osmolality_explanation(params)
    bun = unit_converter_new.conversion_explanation(7.0, "bun", 28.02, None, "mmol/L", "mg/dL")[1]
    expected = round_number(2 * 140 + bun / 2.8 + 90 / 18)
    assert result["Answer"] == expected


def test_serum_osmolality_glucose_mmol_per_l():
    params = {
        "sodium": [140, "mmol/L"],
        "bun": [14, "mg/dL"],
        "glucose": [5.0, "mmol/L"],
    }
    result = sOsm.compute_serum_osmolality_explanation(params)
    glucose = unit_converter_new.conversion_explanation(5.0, "glucose", 180.16, None, "mmol/L", "mg/dL")[1]
    expected = round_number(2 * 140 + 14 / 2.8 + glucose / 18)
    assert result["Answer"] == expected


def test_serum_osmolality_sodium_meq_per_l():
    params = {
        "sodium": [140, "mEq/L"],
        "bun": [14, "mg/dL"],
        "glucose": [90, "mg/dL"],
    }
    result = sOsm.compute_serum_osmolality_explanation(params)
    sodium = unit_converter_new.conversion_explanation(140, "sodium", 22.99, 1, "mEq/L", "mmol/L")[1]
    expected = round_number(2 * sodium + 14 / 2.8 + 90 / 18)
    assert result["Answer"] == expected


def test_serum_osmolality_all_mmol_inputs():
    # Mixed-unit path: Na as mEq/L, BUN/glucose as mmol/L.
    params = {
        "sodium": [140, "mEq/L"],
        "bun": [7.0, "mmol/L"],
        "glucose": [5.0, "mmol/L"],
    }
    result = sOsm.compute_serum_osmolality_explanation(params)
    sodium = unit_converter_new.conversion_explanation(140, "sodium", 22.99, 1, "mEq/L", "mmol/L")[1]
    bun = unit_converter_new.conversion_explanation(7.0, "bun", 28.02, None, "mmol/L", "mg/dL")[1]
    glucose = unit_converter_new.conversion_explanation(5.0, "glucose", 180.16, None, "mmol/L", "mg/dL")[1]
    expected = round_number(2 * sodium + bun / 2.8 + glucose / 18)
    assert result["Answer"] == expected


def test_serum_osmolality_zero_values():
    params = {
        "sodium": [0, "mmol/L"],
        "bun": [0, "mg/dL"],
        "glucose": [0, "mg/dL"],
    }
    result = sOsm.compute_serum_osmolality_explanation(params)
    assert result["Answer"] == 0


def test_sodium_correction_hyperglycemia():
    params = {
        "sodium": [130, "mEq/L"],
        "glucose": [200, "mg/dL"],
    }
    result = sodium_correction_hyperglycemia.compute_sodium_correction_hyperglycemia_explanation(params)
    assert result["Answer"] == round_number(130 + 0.024 * (200 - 100))


def test_sodium_correction_hyperglycemia_glucose_mmol_l():
    params = {
        "sodium": [130, "mEq/L"],
        "glucose": [11.1, "mmol/L"],
    }
    result = sodium_correction_hyperglycemia.compute_sodium_correction_hyperglycemia_explanation(params)
    glucose = unit_converter_new.conversion_explanation(11.1, "glucose", 180.16, None, "mmol/L", "mg/dL")[1]
    assert result["Answer"] == round_number(130 + 0.024 * (glucose - 100))


def test_sodium_correction_hyperglycemia_sodium_mmol_l():
    params = {
        "sodium": [130, "mmol/L"],
        "glucose": [200, "mg/dL"],
    }
    result = sodium_correction_hyperglycemia.compute_sodium_correction_hyperglycemia_explanation(params)
    sodium = unit_converter_new.conversion_explanation(130, "sodium", 22.99, 1, "mmol/L", "mEq/L")[1]
    assert result["Answer"] == round_number(sodium + 0.024 * (200 - 100))


def test_sodium_correction_hyperglycemia_glucose_100_no_change():
    params = {
        "sodium": [130, "mEq/L"],
        "glucose": [100, "mg/dL"],
    }
    result = sodium_correction_hyperglycemia.compute_sodium_correction_hyperglycemia_explanation(params)
    assert result["Answer"] == 130


def test_sodium_correction_hyperglycemia_glucose_low():
    params = {
        "sodium": [130, "mEq/L"],
        "glucose": [80, "mg/dL"],
    }
    result = sodium_correction_hyperglycemia.compute_sodium_correction_hyperglycemia_explanation(params)
    assert result["Answer"] == round_number(130 + 0.024 * (80 - 100))


def test_sodium_correction_hyperglycemia_glucose_low_mmol_l():
    params = {
        "sodium": [130, "mEq/L"],
        "glucose": [5.0, "mmol/L"],
    }
    result = sodium_correction_hyperglycemia.compute_sodium_correction_hyperglycemia_explanation(params)
    glucose = unit_converter_new.conversion_explanation(5.0, "glucose", 180.16, None, "mmol/L", "mg/dL")[1]
    assert result["Answer"] == round_number(130 + 0.024 * (glucose - 100))


def test_free_water_deficit():
    params = {
        "age": [30, "years"],
        "sex": "Male",
        "weight": [70, "kg"],
        "sodium": [150, "mmol/L"],
    }
    result = free_water_deficit.free_water_deficit_explanation(params)
    expected = round_number(0.6 * 70 * (150 / 140 - 1))
    assert result["Answer"] == expected


def test_free_water_deficit_sodium_meq_per_l():
    params = {
        "age": [30, "years"],
        "sex": "Male",
        "weight": [70, "kg"],
        "sodium": [150, "mEq/L"],
    }
    result = free_water_deficit.free_water_deficit_explanation(params)
    sodium = unit_converter_new.conversion_explanation(150, "sodium", 22.99, 1, "mEq/L", "mmol/L")[1]
    expected = round_number(0.6 * 70 * (sodium / 140 - 1))
    assert result["Answer"] == expected


def test_free_water_deficit_female():
    params = {
        "age": [30, "years"],
        "sex": "Female",
        "weight": [70, "kg"],
        "sodium": [150, "mmol/L"],
    }
    result = free_water_deficit.free_water_deficit_explanation(params)
    expected = round_number(0.5 * 70 * (150 / 140 - 1))
    assert result["Answer"] == expected


def test_free_water_deficit_child():
    params = {
        "age": [10, "years"],
        "sex": "Male",
        "weight": [30, "kg"],
        "sodium": [150, "mmol/L"],
    }
    result = free_water_deficit.free_water_deficit_explanation(params)
    expected = round_number(0.6 * 30 * (150 / 140 - 1))
    assert result["Answer"] == expected


def test_free_water_deficit_elderly_male():
    params = {
        "age": [70, "years"],
        "sex": "Male",
        "weight": [70, "kg"],
        "sodium": [150, "mmol/L"],
    }
    result = free_water_deficit.free_water_deficit_explanation(params)
    expected = round_number(0.5 * 70 * (150 / 140 - 1))
    assert result["Answer"] == expected


def test_free_water_deficit_elderly_female():
    params = {
        "age": [70, "years"],
        "sex": "Female",
        "weight": [70, "kg"],
        "sodium": [150, "mmol/L"],
    }
    result = free_water_deficit.free_water_deficit_explanation(params)
    expected = round_number(0.45 * 70 * (150 / 140 - 1))
    assert result["Answer"] == expected


def test_calcium_correction():
    params = {
        "albumin": [3.0, "g/dL"],
        "calcium": [8.0, "mg/dL"],
    }
    result = calcium_correction.calculate_corrected_calcium_explanation(params)
    assert result["Answer"] == round_number(0.8 * (4.0 - 3.0) + 8.0)


def test_calcium_correction_unit_conversions():
    params = {
        "albumin": [35.0, "g/L"],
        "calcium": [2.25, "mmol/L"],
    }
    result = calcium_correction.calculate_corrected_calcium_explanation(params)
    albumin = unit_converter_new.conversion_explanation(35.0, "albmumin", 66500, None, "g/L", "g/dL")[1]
    calcium = unit_converter_new.conversion_explanation(2.25, "calcium", 40.08, 2, "mmol/L", "mg/dL")[1]
    expected = round_number(0.8 * (4.0 - albumin) + calcium)
    assert result["Answer"] == expected


def test_ldl_calculated():
    params = {
        "total_cholesterol": [200, "mg/dL"],
        "hdl_cholesterol": [50, "mg/dL"],
        "triglycerides": [150, "mg/dL"],
    }
    result = ldl_calculated.compute_ldl_explanation(params)
    assert result["Answer"] == round_number(200 - 50 - (150 / 5))


def test_ldl_calculated_mmol_per_l():
    params = {
        "total_cholesterol": [5.17, "mmol/L"],
        "hdl_cholesterol": [1.29, "mmol/L"],
        "triglycerides": [1.7, "mmol/L"],
    }
    result = ldl_calculated.compute_ldl_explanation(params)
    expected_total = unit_converter_new.conversion_explanation(5.17, "total cholesterol", 386.654, None, "mmol/L", "mg/dL")[1]
    expected_hdl = unit_converter_new.conversion_explanation(1.29, "hdl cholesterol", 386.654, None, "mmol/L", "mg/dL")[1]
    expected_trig = unit_converter_new.conversion_explanation(1.7, "triglycerides", 861.338, None, "mmol/L", "mg/dL")[1]
    assert result["Answer"] == round_number(expected_total - expected_hdl - (expected_trig / 5))


def test_ldl_calculated_warns_high_triglycerides():
    params = {
        "total_cholesterol": [200, "mg/dL"],
        "hdl_cholesterol": [50, "mg/dL"],
        "triglycerides": [400, "mg/dL"],
    }
    result = ldl_calculated.compute_ldl_explanation(params)
    assert result["Answer"] == round_number(200 - 50 - (400 / 5))
    assert "Warning" in result["Explanation"]


def test_ldl_calculated_no_warning_below_threshold():
    params = {
        "total_cholesterol": [200, "mg/dL"],
        "hdl_cholesterol": [50, "mg/dL"],
        "triglycerides": [399, "mg/dL"],
    }
    result = ldl_calculated.compute_ldl_explanation(params)
    assert result["Answer"] == round_number(200 - 50 - (399 / 5))
    assert "Warning" not in result["Explanation"]


def test_homa_ir():
    params = {
        "insulin": [10, "µIU/mL"],
        "glucose": [90, "mg/dL"],
    }
    result = homa_ir.compute_homa_ir_explanation(params)
    assert result["Answer"] == round_number((10 * 90) / 405)


def test_homa_ir_glucose_mmol_l():
    params = {
        "insulin": [10, "µIU/mL"],
        "glucose": [5.0, "mmol/L"],
    }
    result = homa_ir.compute_homa_ir_explanation(params)
    glucose = unit_converter_new.conversion_explanation(5.0, "glucose", 180.16, None, "mmol/L", "mg/dL")[1]
    assert result["Answer"] == round_number((10 * glucose) / 405)


def test_homa_ir_pmol_per_l():
    params = {
        "insulin": [5, "pmol/L"],
        "glucose": [100, "mg/dL"],
    }
    result = homa_ir.compute_homa_ir_explanation(params)
    expected = round_number((5 / 6 * 100) / 405)
    assert result["Answer"] == expected


def test_homa_ir_ng_per_ml():
    params = {
        "insulin": [2, "ng/mL"],
        "glucose": [110, "mg/dL"],
    }
    result = homa_ir.compute_homa_ir_explanation(params)
    expected = round_number((2 * 24.8 * 110) / 405)
    assert result["Answer"] == expected


def test_fena():
    params = {
        "sodium": [140, "mEq/L"],
        "creatinine": [1.0, "mg/dL"],
        "urine_sodium": [20, "mEq/L"],
        "urine_creatinine": [100, "mg/dL"],
    }
    result = compute_fena.compute_fena_explanation(params)
    expected = round_number((1.0 * 20) / (140 * 100) * 100)
    assert result["Answer"] == expected


def test_fena_unit_conversions():
    params = {
        "sodium": [140, "mmol/L"],
        "creatinine": [88.4, "µmol/L"],
        "urine_sodium": [20, "mmol/L"],
        "urine_creatinine": [8840, "µmol/L"],
    }
    result = compute_fena.compute_fena_explanation(params)
    sodium = unit_converter_new.conversion_explanation(140, "sodium", 22.99, 1, "mmol/L", "mEq/L")[1]
    creatinine = unit_converter_new.conversion_explanation(88.4, "creatinine", 113.12, 1, "µmol/L", "mg/dL")[1]
    urine_sodium = unit_converter_new.conversion_explanation(20, "urine sodium", 22.99, 1, "mmol/L", "mEq/L")[1]
    urine_creatinine = unit_converter_new.conversion_explanation(8840, "urine creatinine", 113.12, 1, "µmol/L", "mg/dL")[1]
    expected = round_number((creatinine * urine_sodium) / (sodium * urine_creatinine) * 100)
    assert result["Answer"] == expected


def test_creatinine_clearance_normal_weight():
    params = {
        "weight": [70, "kg"],
        "height": [70, "in"],
        "sex": "Male",
        "age": [40, "years"],
        "creatinine": [1.0, "mg/dL"],
    }
    result = creatinine_clearance.generate_cockcroft_gault_explanation(params)
    expected = round_number(((140 - 40) * 70 * 1) / (1.0 * 72))
    assert result["Answer"] == expected


def test_creatinine_clearance_creatinine_umol_l():
    params = {
        "weight": [70, "kg"],
        "height": [70, "in"],
        "sex": "Male",
        "age": [40, "years"],
        "creatinine": [88.4, "µmol/L"],
    }
    result = creatinine_clearance.generate_cockcroft_gault_explanation(params)
    creatinine = unit_converter_new.conversion_explanation(88.4, "creatinine", 113.12, None, "µmol/L", "mg/dL")[1]
    expected = round_number(((140 - 40) * 70 * 1) / (creatinine * 72))
    assert result["Answer"] == expected


def test_mdrd_gfr():
    params = {
        "sex": "Male",
        "age": [40, "years"],
        "creatinine": [1.0, "mg/dL"],
    }
    result = _mdrd_fn()(params)
    expected = round_number(175 * math.exp(math.log(1.0) * -1.154) * math.exp(math.log(40) * -0.203))
    assert result["Answer"] == expected


def test_mdrd_gfr_creatinine_umol_l():
    params = {
        "sex": "Male",
        "age": [40, "years"],
        "creatinine": [88.4, "µmol/L"],
    }
    result = _mdrd_fn()(params)
    creatinine = unit_converter_new.conversion_explanation(88.4, "Creatinine", 113.12, None, "µmol/L", "mg/dL")[1]
    expected = round_number(175 * math.exp(math.log(creatinine) * -1.154) * math.exp(math.log(40) * -0.203))
    assert result["Answer"] == expected


def test_mdrd_gfr_female():
    params = {
        "sex": "Female",
        "age": [40, "years"],
        "creatinine": [1.0, "mg/dL"],
    }
    result = _mdrd_fn()(params)
    base = 175 * math.exp(math.log(1.0) * -1.154) * math.exp(math.log(40) * -0.203)
    expected = round_number(base * 0.742)
    assert result["Answer"] == expected


def test_mdrd_gfr_black_race():
    params = {
        "sex": "Male",
        "age": [40, "years"],
        "creatinine": [1.0, "mg/dL"],
        "race": "Black",
    }
    result = _mdrd_fn()(params)
    base = 175 * math.exp(math.log(1.0) * -1.154) * math.exp(math.log(40) * -0.203)
    expected = round_number(base * 1.212)
    assert result["Answer"] == expected


def test_mdrd_gfr_non_black_race():
    params = {
        "sex": "Male",
        "age": [40, "years"],
        "creatinine": [1.0, "mg/dL"],
        "race": "Asian",
    }
    result = _mdrd_fn()(params)
    expected = round_number(175 * math.exp(math.log(1.0) * -1.154) * math.exp(math.log(40) * -0.203))
    assert result["Answer"] == expected


def test_ckd_epi_2021():
    params = {
        "sex": "Female",
        "age": [40, "years"],
        "creatinine": [0.7, "mg/dL"],
    }
    ckd_module = _load_ckd_epi_module()
    result = ckd_module.ckd_epi_2021_explanation(params)
    expected = round_number(142 * (0.7 / 0.7) ** -0.241 * (0.9938 ** 40) * 1.012)
    assert result["Answer"] == expected


def test_ckd_epi_2021_female_below_threshold():
    params = {
        "sex": "Female",
        "age": [40, "years"],
        "creatinine": [0.69, "mg/dL"],
    }
    ckd_module = _load_ckd_epi_module()
    result = ckd_module.ckd_epi_2021_explanation(params)
    expected = round_number(142 * (0.69 / 0.7) ** -0.241 * (0.9938 ** 40) * 1.012)
    assert result["Answer"] == expected


def test_ckd_epi_2021_female_above_threshold():
    params = {
        "sex": "Female",
        "age": [40, "years"],
        "creatinine": [0.71, "mg/dL"],
    }
    ckd_module = _load_ckd_epi_module()
    result = ckd_module.ckd_epi_2021_explanation(params)
    expected = round_number(142 * (0.71 / 0.7) ** -1.2 * (0.9938 ** 40) * 1.012)
    assert result["Answer"] == expected


def test_ckd_epi_2021_umol_per_l():
    params = {
        "sex": "Female",
        "age": [40, "years"],
        "creatinine": [61.9, "µmol/L"],
    }
    ckd_module = _load_ckd_epi_module()
    result = ckd_module.ckd_epi_2021_explanation(params)
    expected = round_number(142 * (0.7 / 0.7) ** -0.241 * (0.9938 ** 40) * 1.012)
    assert result["Answer"] == expected


def test_ckd_epi_2021_female_high_creatinine():
    params = {
        "sex": "Female",
        "age": [50, "years"],
        "creatinine": [0.9, "mg/dL"],
    }
    ckd_module = _load_ckd_epi_module()
    result = ckd_module.ckd_epi_2021_explanation(params)
    expected = round_number(142 * (0.9 / 0.7) ** -1.2 * (0.9938 ** 50) * 1.012)
    assert result["Answer"] == expected


def test_ckd_epi_2021_male_low_creatinine():
    params = {
        "sex": "Male",
        "age": [60, "years"],
        "creatinine": [0.9, "mg/dL"],
    }
    ckd_module = _load_ckd_epi_module()
    result = ckd_module.ckd_epi_2021_explanation(params)
    expected = round_number(142 * (0.9 / 0.9) ** -0.302 * (0.9938 ** 60) * 1.0)
    assert result["Answer"] == expected


def test_ckd_epi_2021_male_below_threshold():
    params = {
        "sex": "Male",
        "age": [60, "years"],
        "creatinine": [0.89, "mg/dL"],
    }
    ckd_module = _load_ckd_epi_module()
    result = ckd_module.ckd_epi_2021_explanation(params)
    expected = round_number(142 * (0.89 / 0.9) ** -0.302 * (0.9938 ** 60) * 1.0)
    assert result["Answer"] == expected


def test_ckd_epi_2021_male_above_threshold():
    params = {
        "sex": "Male",
        "age": [60, "years"],
        "creatinine": [0.91, "mg/dL"],
    }
    ckd_module = _load_ckd_epi_module()
    result = ckd_module.ckd_epi_2021_explanation(params)
    expected = round_number(142 * (0.91 / 0.9) ** -1.2 * (0.9938 ** 60) * 1.0)
    assert result["Answer"] == expected


def test_ckd_epi_2021_male_umol_per_l():
    params = {
        "sex": "Male",
        "age": [60, "years"],
        "creatinine": [79.6, "µmol/L"],
    }
    ckd_module = _load_ckd_epi_module()
    result = ckd_module.ckd_epi_2021_explanation(params)
    expected = round_number(142 * (0.9 / 0.9) ** -0.302 * (0.9938 ** 60) * 1.0)
    assert result["Answer"] == expected


def test_ckd_epi_2021_male_high_creatinine():
    params = {
        "sex": "Male",
        "age": [60, "years"],
        "creatinine": [1.2, "mg/dL"],
    }
    ckd_module = _load_ckd_epi_module()
    result = ckd_module.ckd_epi_2021_explanation(params)
    expected = round_number(142 * (1.2 / 0.9) ** -1.2 * (0.9938 ** 60) * 1.0)
    assert result["Answer"] == expected


def test_fibrosis_4():
    params = {
        "age": [50, "years"],
        "ast": [30, "U/L"],
        "alt": [40, "U/L"],
        "platelet_count": [200000, "µL"],
    }
    result = fibrosis_4.compute_fib4_explanation(params)
    # 200000 per uL -> 200000 * 1e6 per L = 2e11 => 200 billions
    expected = round_number((50 * 30) / (200 * math.sqrt(40)))
    assert result["Answer"] == expected


def test_meldna_low_values():
    params = {
        "creatinine": [1.0, "mg/dL"],
        "bilirubin": [1.0, "mg/dL"],
        "inr": 1.0,
        "sodium": [137, "mEq/L"],
        "albumin": [3.5, "g/dL"],
        "age": [40, "years"],
        "sex": "Male",
    }
    result = meldna.compute_meldna_explanation(params)
    assert result["Answer"] == 6
