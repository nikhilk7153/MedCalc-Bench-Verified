def compute_wells_criteria_dvt(bedridden_for_atleast_3_days=False, major_surgery_in_last_12_weeks=False, active_cancer=False, calf_swelling_3cm=False, collateral_superficial_veins=False, leg_swollen=False, localized_tenderness_on_deep_venuous_system=False, pitting_edema_on_symptomatic_leg=False, paralysis_paresis_immobilization_in_lower_extreme=False, previous_dvt_documented=False, alternative_to_dvt_diagnosis=False):
    score = 0
    score += 1 if active_cancer else 0
    score += 1 if bedridden_for_atleast_3_days or major_surgery_in_last_12_weeks else 0
    score += 1 if calf_swelling_3cm else 0
    score += 1 if collateral_superficial_veins else 0
    score += 1 if leg_swollen else 0
    score += 1 if localized_tenderness_on_deep_venuous_system else 0
    score += 1 if pitting_edema_on_symptomatic_leg else 0
    score += 1 if paralysis_paresis_immobilization_in_lower_extreme else 0
    score += 1 if previous_dvt_documented else 0
    score -= 2 if alternative_to_dvt_diagnosis else 0
    return score
