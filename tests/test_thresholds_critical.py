from __future__ import annotations

import pytest

import apache_ii
import psi_score
import sofa


def apache_base():
    return {
        "age": [30, "years"],
        "sex": "Male",
        "sodium": [140, "mmol/L"],
        "pH": 7.4,
        "heart_rate": [80, "beats/min"],
        "respiratory_rate": [16, "breaths/min"],
        "potassium": [4.0, "mmol/L"],
        "creatinine": [1.0, "mg/dL"],
        "acute_renal_failure": False,
        "chronic_renal_failure": False,
        "hematocrit": [40, "%"],
        "wbc": [7e9, "L"],
        "fio2": [40, "%"],
        "pao2": [80, "mm Hg"],
        "gcs": 15,
        "sys_bp": [120, "mm Hg"],
        "dia_bp": [80, "mm Hg"],
        "temperature": [98.6, "degrees fahrenheit"],
    }


def apache_score(overrides):
    params = apache_base()
    params.update(overrides)
    return apache_ii.apache_ii_explanation(params)["Answer"]


@pytest.mark.parametrize(
    "age, expected",
    [(44, 0), (45, 2), (55, 3), (65, 5), (75, 6)],
)
def test_apache_age_thresholds(age, expected):
    assert apache_score({"age": [age, "years"]}) == expected


@pytest.mark.parametrize(
    "temp_c, expected",
    [(36.0, 0), (34.0, 1), (32.0, 2), (30.0, 3), (29.0, 4), (38.5, 1), (39.0, 3), (41.0, 4)],
)
def test_apache_temperature_thresholds(temp_c, expected):
    assert apache_score({"temperature": [temp_c, "degrees celsius"]}) == expected


@pytest.mark.parametrize(
    "sys_bp, dia_bp, expected",
    [(120, 80, 0), (150, 90, 2), (190, 100, 3), (220, 130, 4), (90, 45, 2), (60, 40, 4)],
)
def test_apache_map_thresholds(sys_bp, dia_bp, expected):
    assert apache_score({"sys_bp": [sys_bp, "mm Hg"], "dia_bp": [dia_bp, "mm Hg"]}) == expected


@pytest.mark.parametrize(
    "heart_rate, expected",
    [(70, 0), (55, 2), (45, 3), (39, 4), (110, 2), (140, 3), (180, 4)],
)
def test_apache_heart_rate_thresholds(heart_rate, expected):
    assert apache_score({"heart_rate": [heart_rate, "beats/min"]}) == expected


@pytest.mark.parametrize(
    "resp_rate, expected",
    [(12, 0), (10, 1), (6, 2), (5, 4), (25, 1), (35, 3), (50, 4)],
)
def test_apache_respiratory_rate_thresholds(resp_rate, expected):
    assert apache_score({"respiratory_rate": [resp_rate, "breaths/min"]}) == expected


@pytest.mark.parametrize(
    "ph, expected",
    [(7.4, 0), (7.5, 1), (7.6, 3), (7.7, 4), (7.33, 0), (7.25, 2), (7.15, 3), (7.14, 4)],
)
def test_apache_ph_thresholds(ph, expected):
    assert apache_score({"pH": ph}) == expected


@pytest.mark.parametrize(
    "sodium, expected",
    [(140, 0), (150, 1), (155, 2), (160, 3), (180, 4), (120, 2), (111, 3), (110, 4)],
)
def test_apache_sodium_thresholds(sodium, expected):
    assert apache_score({"sodium": [sodium, "mmol/L"]}) == expected


@pytest.mark.parametrize(
    "potassium, expected",
    [(4.0, 0), (5.5, 1), (6.0, 3), (7.0, 4), (3.0, 1), (2.5, 2), (2.4, 4)],
)
def test_apache_potassium_thresholds(potassium, expected):
    assert apache_score({"potassium": [potassium, "mmol/L"]}) == expected


@pytest.mark.parametrize(
    "creatinine, arf, crf, expected",
    [(3.5, True, False, 8), (3.5, False, True, 4), (3.5, False, False, 4), (0.5, False, False, 2)],
)
def test_apache_creatinine_thresholds(creatinine, arf, crf, expected):
    assert apache_score({"creatinine": [creatinine, "mg/dL"], "acute_renal_failure": arf, "chronic_renal_failure": crf}) == expected


@pytest.mark.parametrize(
    "hematocrit, expected",
    [(40, 0), (46, 1), (50, 2), (60, 4), (20, 2), (19, 4)],
)
def test_apache_hematocrit_thresholds(hematocrit, expected):
    assert apache_score({"hematocrit": [hematocrit, "%"]}) == expected


@pytest.mark.parametrize(
    "wbc, expected",
    [(7e9, 0), (15e9, 1), (20e9, 2), (40e9, 4), (2e9, 2), (0.9e9, 4)],
)
def test_apache_wbc_thresholds(wbc, expected):
    assert apache_score({"wbc": [wbc, "L"]}) == expected


def test_apache_oxygenation_fio2_ge_50():
    assert apache_score({"fio2": [60, "%"], "a_a_gradient": 350}) == 3
    assert apache_score({"fio2": [60, "%"], "a_a_gradient": 500}) == 4
    assert apache_score({"fio2": [60, "%"], "a_a_gradient": 199}) == 0


def test_apache_oxygenation_fio2_lt_50():
    assert apache_score({"fio2": [40, "%"], "pao2": [70, "mm Hg"]}) == 1
    assert apache_score({"fio2": [40, "%"], "pao2": [61, "mm Hg"]}) == 1
    assert apache_score({"fio2": [40, "%"], "pao2": [55, "mm Hg"]}) == 3
    assert apache_score({"fio2": [40, "%"], "pao2": [54, "mm Hg"]}) == 4


def test_apache_gcs():
    assert apache_score({"gcs": 15}) == 0
    assert apache_score({"gcs": 12}) == 3


def test_apache_organ_failure_immunocompromise_nonoperative():
    assert apache_score({"organ_failure_immunocompromise": True, "surgery_type": "Nonoperative"}) == 5


def test_apache_organ_failure_immunocompromise_elective():
    assert apache_score({"organ_failure_immunocompromise": True, "surgery_type": "Elective"}) == 2


def sofa_base():
    return {
        "pao2": [400, "mm Hg"],
        "fio2": [100, "%"],
        "platelet_count": [200000, "µL"],
        "bilirubin": [1.0, "mg/dL"],
        "creatinine": [1.0, "mg/dL"],
    }


def sofa_score(overrides):
    params = sofa_base()
    params.update(overrides)
    return sofa.compute_sofa_explanation(params)["Answer"]


@pytest.mark.parametrize(
    "pao2, fio2, expected",
    [(400, 100, 0), (350, 100, 1), (250, 100, 2)],
)
def test_sofa_ratio_thresholds(pao2, fio2, expected):
    assert sofa_score({"pao2": [pao2, "mm Hg"], "fio2": [fio2, "%"]}) == expected


def test_sofa_ratio_with_ventilation():
    assert sofa_score({"pao2": [150, "mm Hg"], "fio2": [100, "%"], "mechanical_ventilation": True}) == 3
    assert sofa_score({"pao2": [90, "mm Hg"], "fio2": [100, "%"], "cpap": True}) == 4


def test_sofa_vasopressors():
    assert sofa_score({"dopamine": [6], "dobutamine": [0]}) == 3
    assert sofa_score({"dopamine": [16]}) == 4
    assert sofa_score({"dobutamine": [1]}) == 2


def test_sofa_vasopressors_epinephrine_norepinephrine_thresholds():
    assert sofa_score({"epinephrine": [0.11]}) == 4
    assert sofa_score({"norepinephrine": [0.05]}) == 3


@pytest.mark.parametrize(
    "gcs, expected",
    [(15, 0), (13, 1), (10, 2), (6, 3), (5, 4)],
)
def test_sofa_gcs_thresholds(gcs, expected):
    assert sofa_score({"gcs": gcs}) == expected


@pytest.mark.parametrize(
    "bilirubin, expected",
    [(1.1, 0), (1.2, 1), (2.0, 2), (6.0, 3), (12.0, 4)],
)
def test_sofa_bilirubin_thresholds(bilirubin, expected):
    assert sofa_score({"bilirubin": [bilirubin, "mg/dL"]}) == expected


@pytest.mark.parametrize(
    "platelets, expected",
    [(150000, 0), (100000, 1), (50000, 2), (20000, 3), (19000, 4)],
)
def test_sofa_platelet_thresholds(platelets, expected):
    assert sofa_score({"platelet_count": [platelets, "µL"]}) == expected


@pytest.mark.parametrize(
    "creatinine, expected",
    [(1.1, 0), (1.2, 1), (2.0, 2), (3.5, 3), (5.1, 4)],
)
def test_sofa_creatinine_thresholds(creatinine, expected):
    assert sofa_score({"creatinine": [creatinine, "mg/dL"]}) == expected


def test_sofa_urine_output_thresholds():
    assert sofa_score({"urine_output": [400, "mL/day"], "creatinine": [1.0, "mg/dL"]}) == 3
    assert sofa_score({"urine_output": [150, "mL/day"], "creatinine": [1.0, "mg/dL"]}) == 4


def psi_base():
    # PSI baseline score for this fixture is age (40) with no adjustments.
    return {
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


def psi_score_with(overrides):
    # Helper to keep PSI threshold tests focused on a single override.
    params = psi_base()
    params.update(overrides)
    return psi_score.psi_score_explanation(params)["Answer"]


def test_psi_female_adjustment():
    assert psi_score_with({"sex": "Female"}) == 30


def test_psi_thresholds_key_vitals():
    assert psi_score_with({"heart_rate": [125, "beats/min"]}) == 50
    assert psi_score_with({"temperature": [34.9, "degrees celsius"]}) == 55
    assert psi_score_with({"temperature": [40.0, "degrees celsius"]}) == 55
    assert psi_score_with({"pH": 7.34}) == 70
    assert psi_score_with({"respiratory_rate": [30, "breaths/min"]}) == 60
    assert psi_score_with({"sys_bp": [89, "mm Hg"]}) == 60


def test_psi_thresholds_labs():
    assert psi_score_with({"bun": [30, "mg/dL"]}) == 60
    assert psi_score_with({"bun": [10.8, "mmol/L"]}) == 60
    assert psi_score_with({"sodium": [129, "mmol/L"]}) == 60
    assert psi_score_with({"glucose": [250, "mg/dL"]}) == 50
    assert psi_score_with({"hematocrit": [29, "%"]}) == 50


def test_psi_thresholds_labs_no_points():
    assert psi_score_with({"bun": [29.9, "mg/dL"]}) == 40
    assert psi_score_with({"bun": [10.7, "mmol/L"]}) == 40
    assert psi_score_with({"sodium": [130, "mmol/L"]}) == 40
    assert psi_score_with({"glucose": [249, "mg/dL"]}) == 40
    assert psi_score_with({"hematocrit": [30, "%"]}) == 40


def test_psi_partial_pressure_thresholds():
    assert psi_score_with({"partial_pressure_oxygen": [59, "mm Hg"]}) == 50
    assert psi_score_with({"partial_pressure_oxygen": [7.9, "kPa"]}) == 50


def test_psi_partial_pressure_thresholds_no_points():
    assert psi_score_with({"partial_pressure_oxygen": [60, "mm Hg"]}) == 40
    assert psi_score_with({"partial_pressure_oxygen": [8.0, "kPa"]}) == 40


def test_psi_nursing_home_resident():
    assert psi_score_with({"nursing_home_resident": True}) == 50


def test_psi_nursing_home_resident_false():
    assert psi_score_with({"nursing_home_resident": False}) == 40


def test_psi_comorbidity_false():
    assert psi_score_with({"chf": False}) == 40


@pytest.mark.parametrize(
    "field, points",
    [
        ("neoplastic_disease", 30),
        ("liver_disease", 20),
        ("chf", 10),
        ("cerebrovascular_disease", 10),
        ("renal_disease", 10),
        ("altered_mental_status", 20),
        ("pleural_effusion", 10),
    ],
)
def test_psi_comorbidities(field, points):
    assert psi_score_with({field: True}) == 40 + points
