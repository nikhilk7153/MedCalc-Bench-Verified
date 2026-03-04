import age_conversion
param_full_name = {'surgery_type': 'surgery type', 'major_surgery_last_month': ('major surgery in the last month', 1), 'chf_last_month': ('congestive heart failure in the last month', 1), 'sepsis': ('sepsis in the last month', 1), 'pneumonia': ('pneumonia in the last month', 1), 'immobilizing_plaster_cast': ('immobilizing plaster cast in the last month', 2), 'hip_pelvis_leg_fracture': ('hip, pelvis, or leg fracture in the last month', 5), 'stroke_last_month': ('stroke in the last month', 5), 'multiple_trauma': ('multiple trauma in the last month', 5), 'acute_spinal_chord_injury': ('acute spinal cord injury causing paralysis in the last month', 5), 'varicose_veins': ('varicose veins', 1), 'current_swollen_legs': ('current swollen legs', 1), 'current_central_venuous': ('current central venuous access', 2), 'previous_dvt': ('previous DVT documented', 3), 'previous_pe': ('previous pulmonary embolism documented', 3), 'family_history_thrombosis': ('family history of thrombosis', 3), 'positive_factor_v': ('Positive Factor V Leiden', 3), 'positive_prothrombin': ('Positive prothrombin 20210A', 3), 'serum_homocysteine': ('an elevated serum homocysteine', 3), 'positive_lupus_anticoagulant': ('a positive lupus anticoagulant', 3), 'elevated_anticardiolipin_antibody': ('an elevated anticardiolipin antibody', 3), 'heparin_induced_thrombocytopenia': ('a heparin-induced thrombocytopenia', 3), 'congenital_acquired_thrombophilia': ('other congenital or acquired thrombophilia', 3), 'mobility': 'mobility', 'inflammatory_bowel_disease': ('history of inflammatory bowel disease', 1), 'acute_myocardial_infarction': ('acute Myocardial infarction', 1), 'copd': ('chronic Obstructive Pulmonary Disease', 1), 'malignancy': ('malignancy', 2), 'bmi': 'bmi'}
surgery_type = {'none': 0, 'minor': 1, 'major': 2, 'laparoscopic': 2, 'arthroscopic': 2, 'elective major lower extremity arthroplasty': 5}
mobility = {'normal': 0, 'on bed rest': 1, 'confined to bed >72 hours': 2}

def caprini_score(sex, age, bmi=None, surgery_type_value=None, mobility_value=None, major_surgery_last_month=False, chf_last_month=False, sepsis=False, pneumonia=False, immobilizing_plaster_cast=False, hip_pelvis_leg_fracture=False, stroke_last_month=False, multiple_trauma=False, acute_spinal_chord_injury=False, varicose_veins=False, current_swollen_legs=False, current_central_venuous=False, previous_dvt=False, previous_pe=False, family_history_thrombosis=False, positive_factor_v=False, positive_prothrombin=False, serum_homocysteine=False, positive_lupus_anticoagulant=False, elevated_anticardiolipin_antibody=False, heparin_induced_thrombocytopenia=False, congenital_acquired_thrombophilia=False, inflammatory_bowel_disease=False, acute_myocardial_infarction=False, copd=False, malignancy=False):
    score = 0
    age = age_conversion.age_conversion(age)
    if age <= 40:
        pass
    elif 41 <= age <= 60:
        score += 1
    elif 61 <= age <= 74:
        score += 2
    elif age >= 75:
        score += 3
    if mobility_value is not None:
        score += mobility.get(str(mobility_value).lower(), 0)
    if surgery_type_value is not None:
        score += surgery_type.get(str(surgery_type_value).lower(), 0)
    if bmi is not None:
        bmi_value = bmi[0] if isinstance(bmi, (list, tuple)) else bmi
        if bmi_value > 25:
            score += 1
    score += 1 if major_surgery_last_month else 0
    score += 1 if chf_last_month else 0
    score += 1 if sepsis else 0
    score += 1 if pneumonia else 0
    score += 2 if immobilizing_plaster_cast else 0
    score += 5 if hip_pelvis_leg_fracture else 0
    score += 5 if stroke_last_month else 0
    score += 5 if multiple_trauma else 0
    score += 5 if acute_spinal_chord_injury else 0
    score += 1 if varicose_veins else 0
    score += 1 if current_swollen_legs else 0
    score += 2 if current_central_venuous else 0
    score += 3 if previous_dvt else 0
    score += 3 if previous_pe else 0
    score += 3 if family_history_thrombosis else 0
    score += 3 if positive_factor_v else 0
    score += 3 if positive_prothrombin else 0
    score += 3 if serum_homocysteine else 0
    score += 3 if positive_lupus_anticoagulant else 0
    score += 3 if elevated_anticardiolipin_antibody else 0
    score += 3 if heparin_induced_thrombocytopenia else 0
    score += 3 if congenital_acquired_thrombophilia else 0
    score += 1 if inflammatory_bowel_disease else 0
    score += 1 if acute_myocardial_infarction else 0
    score += 1 if copd else 0
    score += 2 if malignancy else 0
    return score
