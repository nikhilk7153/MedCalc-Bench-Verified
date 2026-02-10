from __future__ import annotations

import pytest

import caprini_score
import centor_score
import cha2ds2_vasc_score
import child_pugh_score
import curb_65
import feverpain
import glasgow_bleeding_score
import glasgow_bleeding_score_urea
import glasgow_coma_score
import has_bled_score
import heart_score
import perc_rule
import unit_converter_new
import wells_criteria_dvt
import wells_criteria_pe


def centor_base(age: int, temp_c: float = 37.0):
    return {
        "age": [age, "years"],
        "temperature": [temp_c, "degrees celsius"],
        "cough_absent": False,
        "tender_lymph_nodes": False,
        "exudate_swelling_tonsils": False,
    }


@pytest.mark.parametrize(
    "age, expected",
    [(3, 1), (14, 1), (15, 0), (44, 0), (45, -1)],
)
def test_centor_age_thresholds(age, expected):
    result = centor_score.compute_centor_score_explanation(centor_base(age))
    assert result["Answer"] == expected


@pytest.mark.parametrize(
    "temp_c, expected",
    [(38.0, 0), (38.1, 1)],
)
def test_centor_temperature_threshold(temp_c, expected):
    params = centor_base(30, temp_c=temp_c)
    result = centor_score.compute_centor_score_explanation(params)
    assert result["Answer"] == expected


def curb_base():
    return {
        "age": [64, "years"],
        "bun": [19.0, "mg/dL"],
        "respiratory_rate": [29, "breaths/min"],
        "sys_bp": [120, "mm Hg"],
        "dia_bp": [80, "mm Hg"],
        "confusion": False,
    }


@pytest.mark.parametrize(
    "age, expected",
    [(64, 0), (65, 1)],
)
def test_curb65_age_threshold(age, expected):
    params = curb_base()
    params["age"] = [age, "years"]
    result = curb_65.curb_65_explanation(params)
    assert result["Answer"] == expected


@pytest.mark.parametrize(
    "bun, expected",
    [(19.0, 0), (20.0, 0), (20.01, 1)],
)
def test_curb65_bun_threshold(bun, expected):
    params = curb_base()
    params["bun"] = [bun, "mg/dL"]
    result = curb_65.curb_65_explanation(params)
    assert result["Answer"] == expected


@pytest.mark.parametrize(
    "bun, expected",
    [(7.1, 0), (7.2, 1)],
)
def test_curb65_bun_threshold_mmol_l(bun, expected):
    params = curb_base()
    params["bun"] = [bun, "mmol/L"]
    result = curb_65.curb_65_explanation(params)
    assert result["Answer"] == expected


@pytest.mark.parametrize(
    "resp, expected",
    [(29, 0), (30, 1)],
)
def test_curb65_resp_threshold(resp, expected):
    params = curb_base()
    params["respiratory_rate"] = [resp, "breaths/min"]
    result = curb_65.curb_65_explanation(params)
    assert result["Answer"] == expected


@pytest.mark.parametrize(
    "sys_bp, dia_bp, expected",
    [(120, 61, 0), (89, 80, 1), (120, 60, 1)],
)
def test_curb65_bp_threshold(sys_bp, dia_bp, expected):
    params = curb_base()
    params["sys_bp"] = [sys_bp, "mm Hg"]
    params["dia_bp"] = [dia_bp, "mm Hg"]
    result = curb_65.curb_65_explanation(params)
    assert result["Answer"] == expected


@pytest.mark.parametrize(
    "confusion, expected",
    [(False, 0), (True, 1)],
)
def test_curb65_confusion(confusion, expected):
    params = curb_base()
    params["confusion"] = confusion
    result = curb_65.curb_65_explanation(params)
    assert result["Answer"] == expected


@pytest.mark.parametrize(
    "age, expected",
    [(40, 0), (41, 1), (61, 2), (75, 3)],
)
def test_caprini_age_thresholds(age, expected):
    params = {"sex": "Male", "age": [age, "years"], "bmi": [25, "kg/m^2"]}
    result = caprini_score.caprini_score_explanation(params)
    assert result["Answer"] == expected


@pytest.mark.parametrize(
    "bmi, expected",
    [(25, 0), (26, 1)],
)
def test_caprini_bmi_threshold(bmi, expected):
    params = {"sex": "Male", "age": [40, "years"], "bmi": [bmi, "kg/m^2"]}
    result = caprini_score.caprini_score_explanation(params)
    assert result["Answer"] == expected


def test_caprini_surgery_and_mobility():
    params = {"sex": "Male", "age": [40, "years"], "surgery_type": "major", "mobility": "on bed rest"}
    result = caprini_score.caprini_score_explanation(params)
    assert result["Answer"] == 3


@pytest.mark.parametrize(
    "age, expected",
    [(65, 0), (66, 1)],
)
def test_has_bled_age_threshold(age, expected):
    params = {"age": [age, "years"], "alcoholic_drinks": "0"}
    result = has_bled_score.compute_has_bled_score_explanation(params)
    assert result["Answer"] == expected


@pytest.mark.parametrize(
    "drinks, expected",
    [(7, 0), (8, 1)],
)
def test_has_bled_drinks_threshold(drinks, expected):
    params = {"age": [30, "years"], "alcoholic_drinks": str(drinks)}
    result = has_bled_score.compute_has_bled_score_explanation(params)
    assert result["Answer"] == expected


@pytest.mark.parametrize(
    "age, expected",
    [(64, 0), (65, 1), (75, 2)],
)
def test_cha2ds2_vasc_age_thresholds(age, expected):
    params = {"age": [age, "years"], "sex": "Male"}
    result = cha2ds2_vasc_score.generate_cha2ds2_vasc_explanation(params)
    assert result["Answer"] == expected


def test_cha2ds2_vasc_female_adds_point():
    params = {"age": [60, "years"], "sex": "Female"}
    result = cha2ds2_vasc_score.generate_cha2ds2_vasc_explanation(params)
    assert result["Answer"] == 1


@pytest.mark.parametrize(
    "inr, expected",
    [(1.6, 1), (1.7, 2), (2.4, 3)],
)
def test_child_pugh_inr_thresholds(inr, expected):
    params = {
        "inr": inr,
        "bilirubin": [1.0, "mg/dL"],
        "albumin": [4.0, "g/dL"],
        "ascites": "absent",
        "encephalopathy": "No Encephalopathy",
    }
    result = child_pugh_score.compute_child_pugh_score_explanation(params)
    assert result["Answer"] == 4 + expected


@pytest.mark.parametrize(
    "bilirubin, expected",
    [(1.9, 1), (2.0, 2), (3.1, 3)],
)
def test_child_pugh_bilirubin_thresholds(bilirubin, expected):
    params = {
        "inr": 1.2,
        "bilirubin": [bilirubin, "mg/dL"],
        "albumin": [4.0, "g/dL"],
        "ascites": "absent",
        "encephalopathy": "No Encephalopathy",
    }
    result = child_pugh_score.compute_child_pugh_score_explanation(params)
    assert result["Answer"] == 4 + expected


@pytest.mark.parametrize(
    "albumin, expected",
    [(3.6, 1), (3.5, 2), (2.7, 3)],
)
def test_child_pugh_albumin_thresholds(albumin, expected):
    params = {
        "inr": 1.2,
        "bilirubin": [1.0, "mg/dL"],
        "albumin": [albumin, "g/dL"],
        "ascites": "absent",
        "encephalopathy": "No Encephalopathy",
    }
    result = child_pugh_score.compute_child_pugh_score_explanation(params)
    assert result["Answer"] == 4 + expected


def test_child_pugh_albumin_g_per_l():
    params = {
        "inr": 1.2,
        "bilirubin": [1.0, "mg/dL"],
        "albumin": [35.0, "g/L"],
        "ascites": "absent",
        "encephalopathy": "No Encephalopathy",
    }
    result = child_pugh_score.compute_child_pugh_score_explanation(params)
    assert result["Answer"] == 6


def test_child_pugh_bilirubin_umol_per_l():
    params = {
        "inr": 1.2,
        "bilirubin": [34.2, "µmol/L"],
        "albumin": [4.0, "g/dL"],
        "ascites": "absent",
        "encephalopathy": "No Encephalopathy",
    }
    result = child_pugh_score.compute_child_pugh_score_explanation(params)
    expected_bilirubin = unit_converter_new.conversion_explanation(34.2, "bilirubin", 548.66, None, "µmol/L", "mg/dL")[1]
    expected_bilirubin_points = 2 if 2 <= expected_bilirubin <= 3 else 1
    expected = 1 + 1 + 1 + 1 + expected_bilirubin_points
    assert result["Answer"] == expected


def test_child_pugh_ascites_and_encephalopathy():
    params = {
        "inr": 1.2,
        "bilirubin": [1.0, "mg/dL"],
        "albumin": [4.0, "g/dL"],
        "ascites": "moderate",
        "encephalopathy": "Grade 3-4",
    }
    result = child_pugh_score.compute_child_pugh_score_explanation(params)
    assert result["Answer"] == 1 + 1 + 1 + 3 + 3


def test_child_pugh_ascites_slight_grade_1_2():
    params = {
        "inr": 1.2,
        "bilirubin": [1.0, "mg/dL"],
        "albumin": [4.0, "g/dL"],
        "ascites": "slight",
        "encephalopathy": "Grade 1-2",
    }
    result = child_pugh_score.compute_child_pugh_score_explanation(params)
    assert result["Answer"] == 1 + 1 + 1 + 2 + 2


def test_child_pugh_missing_ascites_defaults_absent():
    params = {
        "inr": 1.2,
        "bilirubin": [1.0, "mg/dL"],
        "albumin": [4.0, "g/dL"],
        "encephalopathy": "No Encephalopathy",
    }
    result = child_pugh_score.compute_child_pugh_score_explanation(params)
    assert result["Answer"] == 1 + 1 + 1 + 1 + 1


def glasgow_bleeding_base(sex: str):
    return {
        "hemoglobin": [14.0, "g/dL"],
        "bun": [10.0, "mg/dL"],
        "sex": sex,
        "sys_bp": [120, "mm Hg"],
        "heart_rate": [80, "beats/min"],
        "melena_present": False,
        "syncope": False,
        "hepatic_disease_history": False,
        "cardiac_failure": False,
    }


@pytest.mark.parametrize(
    "bun, expected",
    [(18.19, 0), (18.2, 2), (22.4, 3), (28.0, 4), (70.0, 4), (70.1, 6)],
)
def test_glasgow_bleeding_bun_thresholds(bun, expected):
    params = glasgow_bleeding_base("Male")
    params["bun"] = [bun, "mg/dL"]
    result = glasgow_bleeding_score.glasgow_bleeding_score_explanation(params)
    assert result["Answer"] == expected


@pytest.mark.parametrize(
    "hemoglobin, expected",
    [(13.0, 0), (12.5, 1), (10.5, 3), (9.9, 6)],
)
def test_glasgow_bleeding_hemoglobin_male(hemoglobin, expected):
    params = glasgow_bleeding_base("Male")
    params["hemoglobin"] = [hemoglobin, "g/dL"]
    result = glasgow_bleeding_score.glasgow_bleeding_score_explanation(params)
    assert result["Answer"] == expected


@pytest.mark.parametrize(
    "hemoglobin, expected",
    [(12.0, 0), (11.0, 1), (9.9, 6)],
)
def test_glasgow_bleeding_hemoglobin_female(hemoglobin, expected):
    params = glasgow_bleeding_base("Female")
    params["hemoglobin"] = [hemoglobin, "g/dL"]
    result = glasgow_bleeding_score.glasgow_bleeding_score_explanation(params)
    assert result["Answer"] == expected


@pytest.mark.parametrize(
    "sys_bp, expected",
    [(110, 0), (109, 1), (95, 2), (89, 3)],
)
def test_glasgow_bleeding_bp_thresholds(sys_bp, expected):
    params = glasgow_bleeding_base("Male")
    params["sys_bp"] = [sys_bp, "mm Hg"]
    result = glasgow_bleeding_score.glasgow_bleeding_score_explanation(params)
    assert result["Answer"] == expected


@pytest.mark.parametrize(
    "heart_rate, expected",
    [(99, 0), (100, 1)],
)
def test_glasgow_bleeding_hr_thresholds(heart_rate, expected):
    params = glasgow_bleeding_base("Male")
    params["heart_rate"] = [heart_rate, "beats/min"]
    result = glasgow_bleeding_score.glasgow_bleeding_score_explanation(params)
    assert result["Answer"] == expected


def test_glasgow_bleeding_syncope_and_melena():
    params = glasgow_bleeding_base("Male")
    params["syncope"] = True
    params["melena_present"] = True
    result = glasgow_bleeding_score.glasgow_bleeding_score_explanation(params)
    assert result["Answer"] == 3


def glasgow_bleeding_urea_base(sex: str):
    return {
        "hemoglobin": [14.0, "g/dL"],
        "urea": [5.0, "mmol/L"],
        "sex": sex,
        "sys_bp": [120, "mm Hg"],
        "heart_rate": [80, "beats/min"],
        "melena_present": False,
        "syncope": False,
        "hepatic_disease_history": False,
        "cardiac_failure": False,
    }


@pytest.mark.parametrize(
    "urea, expected",
    [(6.4, 0), (6.5, 2), (7.9, 2), (8.0, 3), (9.9, 3), (10.0, 4), (25.0, 4), (25.1, 6)],
)
def test_glasgow_bleeding_urea_thresholds(urea, expected):
    params = glasgow_bleeding_urea_base("Male")
    params["urea"] = [urea, "mmol/L"]
    result = glasgow_bleeding_score_urea.glasgow_bleeding_score_urea_explanation(params)
    assert result["Answer"] == expected


@pytest.mark.parametrize(
    "hemoglobin, expected",
    [(13.0, 0), (12.5, 1), (10.5, 3), (9.9, 6)],
)
def test_glasgow_bleeding_urea_hemoglobin_male(hemoglobin, expected):
    params = glasgow_bleeding_urea_base("Male")
    params["hemoglobin"] = [hemoglobin, "g/dL"]
    result = glasgow_bleeding_score_urea.glasgow_bleeding_score_urea_explanation(params)
    assert result["Answer"] == expected


@pytest.mark.parametrize(
    "hemoglobin, expected",
    [(12.0, 0), (11.0, 1), (9.9, 6)],
)
def test_glasgow_bleeding_urea_hemoglobin_female(hemoglobin, expected):
    params = glasgow_bleeding_urea_base("Female")
    params["hemoglobin"] = [hemoglobin, "g/dL"]
    result = glasgow_bleeding_score_urea.glasgow_bleeding_score_urea_explanation(params)
    assert result["Answer"] == expected


@pytest.mark.parametrize(
    "sys_bp, expected",
    [(110, 0), (109, 1), (95, 2), (89, 3)],
)
def test_glasgow_bleeding_urea_bp_thresholds(sys_bp, expected):
    params = glasgow_bleeding_urea_base("Male")
    params["sys_bp"] = [sys_bp, "mm Hg"]
    result = glasgow_bleeding_score_urea.glasgow_bleeding_score_urea_explanation(params)
    assert result["Answer"] == expected


@pytest.mark.parametrize(
    "heart_rate, expected",
    [(99, 0), (100, 1)],
)
def test_glasgow_bleeding_urea_hr_thresholds(heart_rate, expected):
    params = glasgow_bleeding_urea_base("Male")
    params["heart_rate"] = [heart_rate, "beats/min"]
    result = glasgow_bleeding_score_urea.glasgow_bleeding_score_urea_explanation(params)
    assert result["Answer"] == expected


@pytest.mark.parametrize(
    "age, expected",
    [(44, 0), (45, 1), (65, 2)],
)
def test_heart_score_age_thresholds(age, expected):
    params = {"age": [age, "years"]}
    result = heart_score.compute_heart_score_explanation(params)
    assert result["Answer"] == expected


def test_heart_score_risk_factors_counts():
    params = {
        "age": [30, "years"],
        "hypertension": True,
    }
    result = heart_score.compute_heart_score_explanation(params)
    assert result["Answer"] == 1

    params = {
        "age": [30, "years"],
        "hypertension": True,
        "hypercholesterolemia": True,
        "diabetes_mellitus": True,
    }
    result = heart_score.compute_heart_score_explanation(params)
    assert result["Answer"] == 2


def test_heart_score_troponin_categories():
    params = {"age": [30, "years"], "initial_troponin": "between the normal limit or up to three times the normal limit"}
    result = heart_score.compute_heart_score_explanation(params)
    assert result["Answer"] == 1

    params = {"age": [30, "years"], "initial_troponin": "greater than three times normal limit"}
    result = heart_score.compute_heart_score_explanation(params)
    assert result["Answer"] == 2


@pytest.mark.parametrize(
    "age, hr, o2, expected",
    [
        (49, 99, 95, 0),
        (50, 99, 95, 1),
        (49, 100, 95, 1),
        (49, 99, 94, 1),
    ],
)
def test_perc_rule_thresholds(age, hr, o2, expected):
    params = {
        "age": [age, "years"],
        "heart_rate": [hr, "beats/min"],
        "oxygen_sat": [o2, "%"],
    }
    result = perc_rule.compute_perc_rule_explanation(params)
    assert result["Answer"] == expected


def test_wells_dvt_alternative_and_bedrest():
    params = {
        "alternative_to_dvt_diagnosis": True,
        "bedridden_for_atleast_3_days": True,
        "major_surgery_in_last_12_weeks": False,
    }
    result = wells_criteria_dvt.compute_wells_criteria_dvt_explanation(params)
    assert result["Answer"] == -1


def test_wells_dvt_active_cancer_positive():
    params = {
        "active_cancer": True,
    }
    result = wells_criteria_dvt.compute_wells_criteria_dvt_explanation(params)
    assert result["Answer"] == 1


def test_wells_pe_thresholds():
    params = {"heart_rate": [101, "beats/min"]}
    result = wells_criteria_pe.calculate_pe_wells_explanation(params)
    assert result["Answer"] == 1.5

    params = {
        "heart_rate": [80, "beats/min"],
        "clinical_dvt": True,
    }
    result = wells_criteria_pe.calculate_pe_wells_explanation(params)
    assert result["Answer"] == 3


def test_glasgow_coma_not_testable():
    params = {
        "best_eye_response": "not testable",
        "best_verbal_response": "not testable",
        "best_motor_response": "obeys commands",
    }
    result = glasgow_coma_score.compute_glasgow_coma_score_explanation(params)
    assert result["Answer"] == 6


def test_glasgow_coma_motor_not_testable():
    params = {
        "best_eye_response": "eyes open spontaneously",
        "best_verbal_response": "oriented",
        "best_motor_response": "not testable",
    }
    result = glasgow_coma_score.compute_glasgow_coma_score_explanation(params)
    assert result["Answer"] == 9


def test_feverpain_thresholds():
    params = {
        "fever_24_hours": True,
        "cough_coryza_absent": True,
        "symptom_onset": True,
        "purulent_tonsils": True,
        "severe_tonsil_inflammation": True,
    }
    result = feverpain.compute_fever_pain_explanation(params)
    assert result["Answer"] == 5
