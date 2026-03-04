import os
import json
import unit_converter_new
import age_conversion
import convert_temperature

def psi_score(age, sex, heart_rate, temperature, pH, respiratory_rate, sys_bp, bun, sodium, glucose, hematocrit, partial_pressure_oxygen=None, nursing_home_resident=False, neoplastic_disease=False, liver_disease=False, chf=False, cerebrovascular_disease=False, renal_disease=False, altered_mental_status=False, pleural_effusion=False):
    age_years = age_conversion.age_conversion(age)
    pulse = heart_rate[0]
    temp_c = convert_temperature.fahrenheit_to_celsius(temperature[0], temperature[1])
    rr = respiratory_rate[0]
    sbp = sys_bp[0]
    bun_val = unit_converter_new.conversion(bun[0], 'BUN', 28.02, None, bun[1], 'mg/dL')
    sodium_val = unit_converter_new.conversion(sodium[0], 'sodium', 22.99, 1, sodium[1], 'mmol/L')
    glucose_val = unit_converter_new.conversion(glucose[0], 'glucose', 180.16, None, glucose[1], 'mg/dL')
    hematocrit_val = hematocrit[0]
    score = age_years
    if sex == 'Female':
        score -= 10
    score += 10 if nursing_home_resident else 0
    score += 30 if neoplastic_disease else 0
    score += 20 if liver_disease else 0
    score += 10 if chf else 0
    score += 10 if cerebrovascular_disease else 0
    score += 10 if renal_disease else 0
    score += 20 if altered_mental_status else 0
    score += 10 if pleural_effusion else 0
    score += 10 if pulse >= 125 else 0
    score += 15 if temp_c < 35 or temp_c > 39.9 else 0
    score += 30 if pH < 7.35 else 0
    score += 20 if rr >= 30 else 0
    score += 20 if sbp < 90 else 0
    score += 20 if bun_val >= 30 else 0
    score += 20 if sodium_val < 130 else 0
    score += 10 if glucose_val >= 250 else 0
    score += 10 if hematocrit_val < 30 else 0
    if partial_pressure_oxygen is not None:
        if partial_pressure_oxygen[1] == 'mm Hg' and partial_pressure_oxygen[0] < 60:
            score += 10
        elif partial_pressure_oxygen[1] == 'kPa' and partial_pressure_oxygen[0] < 8:
            score += 10
    return score
