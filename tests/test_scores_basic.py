from __future__ import annotations

import caprini_score
import has_bled_score
import cha2ds2_vasc_score
import cci
import centor_score
import curb_65
import feverpain
import cardiac_risk_index
import child_pugh_score
import glasgow_coma_score
import glasgow_bleeding_score
import glasgow_bleeding_score_urea
import heart_score
import perc_rule
import sirs_criteria
import wells_criteria_dvt
import wells_criteria_pe


def test_caprini_score_minimal():
    params = {"sex": "Male", "age": [50, "years"]}
    result = caprini_score.caprini_score_explanation(params)
    assert result["Answer"] == 1


def test_caprini_score_with_true_false_flags():
    params = {
        "sex": "Male",
        "age": [50, "years"],
        "surgery_type": "minor",
        "mobility": "on bed rest",
        "bmi": [30, "kg/m^2"],
        "varicose_veins": True,
        "current_swollen_legs": False,
        "malignancy": True,
    }
    result = caprini_score.caprini_score_explanation(params)
    assert result["Answer"] == 7


def test_has_bled_score():
    params = {
        "age": [70, "years"],
        "alcoholic_drinks": "9",
    }
    result = has_bled_score.compute_has_bled_score_explanation(params)
    assert result["Answer"] == 2


def test_has_bled_score_explicit_flags():
    params = {
        "age": [70, "years"],
        "alcoholic_drinks": "0",
        "hypertension": False,
        "stroke": True,
    }
    result = has_bled_score.compute_has_bled_score_explanation(params)
    assert result["Answer"] == 2


def test_cha2ds2_vasc_score_base():
    params = {"age": [60, "years"], "sex": "Male"}
    result = cha2ds2_vasc_score.generate_cha2ds2_vasc_explanation(params)
    assert result["Answer"] == 0


def test_cha2ds2_vasc_score_all_factors():
    params = {
        "age": [76, "years"],
        "sex": "Female",
        "chf": True,
        "hypertension": True,
        "stroke": True,
        "tia": False,
        "thromboembolism": False,
        "vascular_disease": True,
        "diabetes": True,
    }
    result = cha2ds2_vasc_score.generate_cha2ds2_vasc_explanation(params)
    assert result["Answer"] == 9


def test_cci_score_base():
    params = {"age": [40, "years"]}
    result = cci.compute_cci_explanation(params)
    assert result["Answer"] == 0


def test_cci_score_age_75():
    params = {"age": [75, "years"]}
    result = cci.compute_cci_explanation(params)
    assert result["Answer"] == 3


def test_cci_score_localized_tumor():
    params = {
        "age": [55, "years"],
        "mi": False,
        "chf": True,
        "peripheral_vascular_disease": True,
        "cva": True,
        "liver_disease": "mild",
        "diabetes_mellitus": "end-organ damage",
        "hemiplegia": True,
        "solid_tumor": "localized",
        "aids": True,
    }
    result = cci.compute_cci_explanation(params)
    assert result["Answer"] == 17


def test_cci_score_metastatic_tumor():
    params = {
        "age": [82, "years"],
        "tia": True,
        "cva": False,
        "liver_disease": "moderate to severe",
        "diabetes_mellitus": "uncomplicated",
        "moderate_to_severe_ckd": True,
        "leukemia": True,
        "lymphoma": True,
        "solid_tumor": "metastatic",
        "peripheral_vascular_disease": True,
    }
    result = cci.compute_cci_explanation(params)
    assert result["Answer"] == 22


def test_cci_score_age_65_none_categories():
    params = {
        "age": [65, "years"],
        "tia": False,
        "cva": False,
        "solid_tumor": "none",
        "liver_disease": "none",
        "diabetes_mellitus": "none or diet-controlled",
    }
    result = cci.compute_cci_explanation(params)
    assert result["Answer"] == 2


def test_centor_score_base():
    params = {
        "age": [30, "years"],
        "temperature": [98.6, "degrees fahrenheit"],
        "cough_absent": False,
        "tender_lymph_nodes": False,
        "exudate_swelling_tonsils": False,
    }
    result = centor_score.compute_centor_score_explanation(params)
    assert result["Answer"] == 0


def test_centor_score_missing_cough_and_exudate_present():
    params = {
        "age": [10, "years"],
        "temperature": [101.0, "degrees fahrenheit"],
        "exudate_swelling_tonsils": True,
    }
    result = centor_score.compute_centor_score_explanation(params)
    assert result["Answer"] == 4


def test_centor_score_cough_absent_and_lymph_nodes_present():
    params = {
        "age": [50, "years"],
        "temperature": [98.6, "degrees fahrenheit"],
        "cough_absent": True,
        "tender_lymph_nodes": True,
        "exudate_swelling_tonsils": False,
    }
    result = centor_score.compute_centor_score_explanation(params)
    assert result["Answer"] == 1


def test_curb_65_score_base():
    params = {
        "age": [50, "years"],
        "bun": [10, "mg/dL"],
        "respiratory_rate": [20, "breaths/min"],
        "sys_bp": [120, "mm Hg"],
        "dia_bp": [80, "mm Hg"],
        "confusion": False,
    }
    result = curb_65.curb_65_explanation(params)
    assert result["Answer"] == 0


def test_curb_65_confusion_missing():
    params = {
        "age": [50, "years"],
        "bun": [10, "mg/dL"],
        "respiratory_rate": [20, "breaths/min"],
        "sys_bp": [120, "mm Hg"],
        "dia_bp": [80, "mm Hg"],
    }
    result = curb_65.curb_65_explanation(params)
    assert result["Answer"] == 0


def test_feverpain_base():
    params = {
        "fever_24_hours": False,
        "cough_coryza_absent": False,
        "symptom_onset": False,
        "purulent_tonsils": False,
        "severe_tonsil_inflammation": False,
    }
    result = feverpain.compute_fever_pain_explanation(params)
    assert result["Answer"] == 0


def test_feverpain_missing_parameter():
    params = {
        "fever_24_hours": False,
        "cough_coryza_absent": False,
        "symptom_onset": False,
        "purulent_tonsils": False,
    }
    result = feverpain.compute_fever_pain_explanation(params)
    assert result["Answer"] == 0


def test_cardiac_risk_index_base():
    params = {"pre_operative_creatinine": [1.0, "mg/dL"]}
    result = cardiac_risk_index.compute_cardiac_index_explanation(params)
    assert result["Answer"] == 0


def test_cardiac_risk_index_congestive_heart_failure():
    params = {
        "congestive_heart_failure": True,
        "pre_operative_creatinine": [1.0, "mg/dL"],
    }
    result = cardiac_risk_index.compute_cardiac_index_explanation(params)
    assert result["Answer"] == 1


def test_cardiac_risk_index_ischemic_heart_disease():
    params = {
        # Implementation key in this revision uses "ischemetic_heart_disease".
        "ischemetic_heart_disease": True,
        "pre_operative_creatinine": [1.0, "mg/dL"],
    }
    result = cardiac_risk_index.compute_cardiac_index_explanation(params)
    assert result["Answer"] == 1


def test_cardiac_risk_index_cerebrovascular_disease():
    params = {
        "cerebrovascular_disease": True,
        "pre_operative_creatinine": [1.0, "mg/dL"],
    }
    result = cardiac_risk_index.compute_cardiac_index_explanation(params)
    assert result["Answer"] == 1


def test_cardiac_risk_index_insulin_treatment():
    params = {
        "pre_operative_insulin_treatment": True,
        "pre_operative_creatinine": [1.0, "mg/dL"],
    }
    result = cardiac_risk_index.compute_cardiac_index_explanation(params)
    assert result["Answer"] == 1


def test_cardiac_risk_index_creatinine_boundary():
    params = {"pre_operative_creatinine": [2.0, "mg/dL"]}
    result = cardiac_risk_index.compute_cardiac_index_explanation(params)
    assert result["Answer"] == 0


def test_cardiac_risk_index_high_creatinine_and_surgery():
    params = {
        "elevated_risk_surgery": True,
        "pre_operative_creatinine": [2.5, "mg/dL"],
    }
    result = cardiac_risk_index.compute_cardiac_index_explanation(params)
    assert result["Answer"] == 2


def test_child_pugh_score_low_risk():
    params = {
        "inr": 1.2,
        "bilirubin": [1.0, "mg/dL"],
        "albumin": [4.0, "g/dL"],
        "ascites": "absent",
    }
    result = child_pugh_score.compute_child_pugh_score_explanation(params)
    assert result["Answer"] == 5


def test_glasgow_coma_score():
    params = {
        "best_eye_response": "eyes open spontaneously",
        "best_verbal_response": "oriented",
        "best_motor_response": "obeys commands",
    }
    result = glasgow_coma_score.compute_glasgow_coma_score_explanation(params)
    assert result["Answer"] == 15


def test_glasgow_coma_score_extension_to_pain():
    params = {
        "best_eye_response": "eye opening to pain",
        "best_verbal_response": "inappropriate words",
        "best_motor_response": "extension to pain",
    }
    result = glasgow_coma_score.compute_glasgow_coma_score_explanation(params)
    assert result["Answer"] == 7


def test_glasgow_bleeding_score_base():
    params = {
        "hemoglobin": [14.0, "g/dL"],
        "bun": [10.0, "mg/dL"],
        "sex": "Male",
        "sys_bp": [120, "mm Hg"],
        "heart_rate": [80, "beats/min"],
        "melena_present": False,
        "syncope": False,
        "hepatic_disease_history": False,
        "cardiac_failure": False,
    }
    result = glasgow_bleeding_score.glasgow_bleeding_score_explanation(params)
    assert result["Answer"] == 0


def test_glasgow_bleeding_bun_mmol_l():
    params = {
        "hemoglobin": [14.0, "g/dL"],
        "bun": [10.7, "mmol/L"],
        "sex": "Male",
        "sys_bp": [120, "mm Hg"],
        "heart_rate": [80, "beats/min"],
        "melena_present": False,
        "syncope": False,
        "hepatic_disease_history": False,
        "cardiac_failure": False,
    }
    result = glasgow_bleeding_score.glasgow_bleeding_score_explanation(params)
    assert result["Answer"] == 4


def test_glasgow_bleeding_hepatic_disease_points():
    params = {
        "hemoglobin": [14.0, "g/dL"],
        "bun": [10.0, "mg/dL"],
        "sex": "Male",
        "sys_bp": [120, "mm Hg"],
        "heart_rate": [80, "beats/min"],
        "melena_present": False,
        "syncope": False,
        "hepatic_disease_history": True,
        "cardiac_failure": False,
    }
    result = glasgow_bleeding_score.glasgow_bleeding_score_explanation(params)
    assert result["Answer"] == 2


def test_glasgow_bleeding_cardiac_failure_points():
    params = {
        "hemoglobin": [14.0, "g/dL"],
        "bun": [10.0, "mg/dL"],
        "sex": "Male",
        "sys_bp": [120, "mm Hg"],
        "heart_rate": [80, "beats/min"],
        "melena_present": False,
        "syncope": False,
        "hepatic_disease_history": False,
        "cardiac_failure": True,
    }
    result = glasgow_bleeding_score.glasgow_bleeding_score_explanation(params)
    assert result["Answer"] == 2


def test_glasgow_bleeding_urea_base():
    params = {
        "hemoglobin": [14.0, "g/dL"],
        "urea": [5.0, "mmol/L"],
        "sex": "Male",
        "sys_bp": [120, "mm Hg"],
        "heart_rate": [80, "beats/min"],
    }
    result = glasgow_bleeding_score_urea.glasgow_bleeding_score_urea_explanation(params)
    assert result["Answer"] == 0


def test_glasgow_bleeding_urea_mg_dl_conversion():
    params = {
        "hemoglobin": [14.0, "g/dL"],
        "urea": [47.45, "mg/dL"],
        "sex": "Male",
        "sys_bp": [120, "mm Hg"],
        "heart_rate": [80, "beats/min"],
        "melena_present": False,
        "syncope": False,
        "hepatic_disease_history": False,
        "cardiac_failure": False,
    }
    result = glasgow_bleeding_score_urea.glasgow_bleeding_score_urea_explanation(params)
    assert result["Answer"] == 2


def test_glasgow_bleeding_urea_hr_boundary():
    params = {
        "hemoglobin": [14.0, "g/dL"],
        "urea": [5.0, "mmol/L"],
        "sex": "Male",
        "sys_bp": [120, "mm Hg"],
        "heart_rate": [100, "beats/min"],
        "melena_present": False,
        "syncope": False,
        "hepatic_disease_history": False,
        "cardiac_failure": False,
    }
    result = glasgow_bleeding_score_urea.glasgow_bleeding_score_urea_explanation(params)
    assert result["Answer"] == 1


def test_glasgow_bleeding_urea_female_hgb_boundary():
    params = {
        "hemoglobin": [12.0, "g/dL"],
        "urea": [5.0, "mmol/L"],
        "sex": "Female",
        "sys_bp": [120, "mm Hg"],
        "heart_rate": [80, "beats/min"],
        "melena_present": False,
        "syncope": False,
        "hepatic_disease_history": False,
        "cardiac_failure": False,
    }
    result = glasgow_bleeding_score_urea.glasgow_bleeding_score_urea_explanation(params)
    assert result["Answer"] == 0


def test_heart_score_base():
    params = {
        "age": [30, "years"],
    }
    result = heart_score.compute_heart_score_explanation(params)
    assert result["Answer"] == 0


def test_heart_score_false_risk_factor():
    params = {
        "age": [30, "years"],
        "diabetes_mellitus": False,
    }
    result = heart_score.compute_heart_score_explanation(params)
    assert result["Answer"] == 0


def test_perc_rule_base():
    params = {
        "age": [30, "years"],
        "heart_rate": [80, "beats/min"],
        "oxygen_sat": [98, "%"],
    }
    result = perc_rule.compute_perc_rule_explanation(params)
    assert result["Answer"] == 0


def test_perc_rule_explicit_false_param():
    params = {
        "age": [30, "years"],
        "heart_rate": [80, "beats/min"],
        "oxygen_sat": [98, "%"],
        "unilateral_leg_swelling": False,
    }
    result = perc_rule.compute_perc_rule_explanation(params)
    assert result["Answer"] == 0


def test_perc_rule_previous_dvt_only():
    params = {
        "age": [60, "years"],
        "heart_rate": [80, "beats/min"],
        "oxygen_sat": [98, "%"],
        "previous_dvt": True,
        "previous_pe": False,
    }
    result = perc_rule.compute_perc_rule_explanation(params)
    assert result["Answer"] == 2


def test_perc_rule_previous_pe_only():
    params = {
        "age": [40, "years"],
        "heart_rate": [80, "beats/min"],
        "oxygen_sat": [94, "%"],
        "previous_dvt": False,
        "previous_pe": True,
        "unilateral_leg_swelling": True,
    }
    result = perc_rule.compute_perc_rule_explanation(params)
    assert result["Answer"] == 3


def test_sirs_criteria_base():
    params = {
        "temperature": [98.6, "degrees fahrenheit"],
        "heart_rate": [80, "beats/min"],
        "wbc": [8000, "mm^3"],
        "respiratory_rate": [16, "breaths/min"],
    }
    result = sirs_criteria.sirs_criteria_explanation(params)
    assert result["Answer"] == 0


def test_sirs_criteria_hr_boundary():
    params = {
        "temperature": [98.6, "degrees fahrenheit"],
        "heart_rate": [90, "beats/min"],
        "wbc": [8000, "mm^3"],
        "respiratory_rate": [16, "breaths/min"],
    }
    result = sirs_criteria.sirs_criteria_explanation(params)
    assert result["Answer"] == 0


def test_sirs_criteria_hr_high():
    params = {
        "temperature": [98.6, "degrees fahrenheit"],
        "heart_rate": [91, "beats/min"],
        "wbc": [8000, "mm^3"],
        "respiratory_rate": [16, "breaths/min"],
    }
    result = sirs_criteria.sirs_criteria_explanation(params)
    assert result["Answer"] == 1


def test_sirs_criteria_paco2_boundary():
    params = {
        "temperature": [98.6, "degrees fahrenheit"],
        "heart_rate": [80, "beats/min"],
        "wbc": [8000, "mm^3"],
        "paco2": [31, "mm Hg"],
    }
    result = sirs_criteria.sirs_criteria_explanation(params)
    assert result["Answer"] == 1


def test_sirs_criteria_high_temp():
    params = {
        "temperature": [102.0, "degrees fahrenheit"],
        "heart_rate": [80, "beats/min"],
        "wbc": [8000, "mm^3"],
        "respiratory_rate": [16, "breaths/min"],
    }
    result = sirs_criteria.sirs_criteria_explanation(params)
    assert result["Answer"] == 1


def test_sirs_criteria_low_temp():
    params = {
        "temperature": [95.0, "degrees fahrenheit"],
        "heart_rate": [80, "beats/min"],
        "wbc": [8000, "mm^3"],
        "respiratory_rate": [16, "breaths/min"],
    }
    result = sirs_criteria.sirs_criteria_explanation(params)
    assert result["Answer"] == 1


def test_sirs_criteria_wbc_high():
    params = {
        "temperature": [98.6, "degrees fahrenheit"],
        "heart_rate": [80, "beats/min"],
        "wbc": [13000, "mm^3"],
        "respiratory_rate": [16, "breaths/min"],
    }
    result = sirs_criteria.sirs_criteria_explanation(params)
    assert result["Answer"] == 1


def test_sirs_criteria_wbc_low():
    params = {
        "temperature": [98.6, "degrees fahrenheit"],
        "heart_rate": [80, "beats/min"],
        "wbc": [3000, "mm^3"],
        "respiratory_rate": [16, "breaths/min"],
    }
    result = sirs_criteria.sirs_criteria_explanation(params)
    assert result["Answer"] == 1


def test_sirs_criteria_resp_rate_high():
    params = {
        "temperature": [98.6, "degrees fahrenheit"],
        "heart_rate": [80, "beats/min"],
        "wbc": [8000, "mm^3"],
        "respiratory_rate": [22, "breaths/min"],
    }
    result = sirs_criteria.sirs_criteria_explanation(params)
    assert result["Answer"] == 1


def test_sirs_criteria_paco2_equal_32():
    params = {
        "temperature": [98.6, "degrees fahrenheit"],
        "heart_rate": [80, "beats/min"],
        "wbc": [8000, "mm^3"],
        "paco2": [32, "mm Hg"],
    }
    result = sirs_criteria.sirs_criteria_explanation(params)
    assert result["Answer"] == 0


def test_sirs_criteria_paco2_above_32():
    params = {
        "temperature": [98.6, "degrees fahrenheit"],
        "heart_rate": [80, "beats/min"],
        "wbc": [8000, "mm^3"],
        "paco2": [40, "mm Hg"],
    }
    result = sirs_criteria.sirs_criteria_explanation(params)
    assert result["Answer"] == 0


def test_sirs_criteria_bands_trigger():
    params = {
        "temperature": [98.6, "degrees fahrenheit"],
        "heart_rate": [80, "beats/min"],
        "wbc": [8000, "mm^3"],
        "bands": [12, "%"],
        "respiratory_rate": [16, "breaths/min"],
    }
    result = sirs_criteria.sirs_criteria_explanation(params)
    assert result["Answer"] == 1


def test_wells_dvt_base():
    result = wells_criteria_dvt.compute_wells_criteria_dvt_explanation({})
    assert result["Answer"] == 0


def test_wells_dvt_collateral_veins():
    params = {"collateral_superficial_veins": True}
    result = wells_criteria_dvt.compute_wells_criteria_dvt_explanation(params)
    assert result["Answer"] == 1


def test_wells_dvt_paralysis_paresis_immobilization():
    params = {"paralysis_paresis_immobilization_in_lower_extreme": True}
    result = wells_criteria_dvt.compute_wells_criteria_dvt_explanation(params)
    assert result["Answer"] == 1


def test_wells_dvt_localized_tenderness():
    params = {"localized_tenderness_on_deep_venuous_system": True}
    result = wells_criteria_dvt.compute_wells_criteria_dvt_explanation(params)
    assert result["Answer"] == 1


def test_wells_dvt_calf_swelling():
    params = {"calf_swelling_3cm": True}
    result = wells_criteria_dvt.compute_wells_criteria_dvt_explanation(params)
    assert result["Answer"] == 1


def test_wells_dvt_pitting_edema():
    params = {"pitting_edema_on_symptomatic_leg": True}
    result = wells_criteria_dvt.compute_wells_criteria_dvt_explanation(params)
    assert result["Answer"] == 1


def test_wells_dvt_entire_leg_swollen():
    params = {"leg_swollen": True}
    result = wells_criteria_dvt.compute_wells_criteria_dvt_explanation(params)
    assert result["Answer"] == 1


def test_wells_dvt_previous_dvt_documented():
    params = {"previous_dvt_documented": True}
    result = wells_criteria_dvt.compute_wells_criteria_dvt_explanation(params)
    assert result["Answer"] == 1


def test_wells_pe_base():
    params = {"heart_rate": [80, "beats/min"]}
    result = wells_criteria_pe.calculate_pe_wells_explanation(params)
    assert result["Answer"] == 0


def test_wells_pe_full_positive():
    params = {
        "clinical_dvt": True,
        "pe_number_one": True,
        "heart_rate": [120, "beats/min"],
        "immobilization_for_3days": True,
        "surgery_in_past4weeks": False,
        "previous_pe": True,
        "previous_dvt": False,
        "hemoptysis": True,
        "malignancy_with_treatment": True,
    }
    result = wells_criteria_pe.calculate_pe_wells_explanation(params)
    assert result["Answer"] == 12.5


def test_wells_pe_false_branches_with_surgery():
    params = {
        "clinical_dvt": False,
        "pe_number_one": False,
        "heart_rate": [80, "beats/min"],
        "immobilization_for_3days": False,
        "surgery_in_past4weeks": True,
        "previous_pe": False,
        "previous_dvt": True,
        "hemoptysis": False,
        "malignancy_with_treatment": False,
    }
    result = wells_criteria_pe.calculate_pe_wells_explanation(params)
    assert result["Answer"] == 3.0


def test_wells_pe_both_immob_and_surgery():
    params = {
        "clinical_dvt": True,
        "pe_number_one": True,
        "heart_rate": [80, "beats/min"],
        "immobilization_for_3days": True,
        "surgery_in_past4weeks": True,
        "previous_pe": True,
        "previous_dvt": True,
    }
    result = wells_criteria_pe.calculate_pe_wells_explanation(params)
    assert result["Answer"] == 9.0
