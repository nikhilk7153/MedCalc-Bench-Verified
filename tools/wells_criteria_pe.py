import os
import json

def calculate_pe_wells(clinical_dvt, pe_number_one, heart_rate, immobilization_for_3days, surgery_in_past4weeks, previous_pe, previous_dvt, hemoptysis, malignancy_with_treatment):
    score = 0
    if clinical_dvt is not None:
        if clinical_dvt:
            score += 3
    if pe_number_one is not None:
        if pe_number_one:
            score += 3
    if heart_rate[0] > 100:
        score += 1.5
    if immobilization_for_3days is None:
        immobilization_for_3days = False
    if surgery_in_past4weeks is None:
        surgery_in_past4weeks = False
    if not immobilization_for_3days and (not surgery_in_past4weeks):
        pass
    elif not immobilization_for_3days and surgery_in_past4weeks:
        score += 1.5
    elif immobilization_for_3days and (not surgery_in_past4weeks):
        score += 1.5
    elif immobilization_for_3days and surgery_in_past4weeks:
        score += 1.5
    if previous_pe is None:
        previous_pe = False
    if previous_dvt is None:
        previous_dvt = False
    if not previous_pe and (not previous_dvt):
        pass
    elif not previous_pe and previous_dvt:
        score += 1.5
    elif previous_pe and (not previous_dvt):
        score += 1.5
    elif previous_pe and previous_dvt:
        score += 1.5
    if hemoptysis is not None:
        if hemoptysis:
            score += 1
    if malignancy_with_treatment is not None:
        if malignancy_with_treatment:
            score += 1
    return score
