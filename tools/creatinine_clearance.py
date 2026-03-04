import weight_conversion
import height_conversion
import ideal_body_weight
import adjusted_body_weight
import bmi_calculator
import unit_converter_new
import age_conversion
from rounding import round_number

def generate_cockcroft_gault(weight, sex, age, creatinine, height):
    raw_weight = weight
    weight = weight_conversion.weight_conversion(weight)
    gender_coefficient = 1 if sex == 'Male' else 0.85
    age = age_conversion.age_conversion(age)
    serum_creatinine_value = creatinine[0]
    serum_creatinine_units = creatinine[1]
    is_male = True if sex == 'Male' else False
    bmi = float(bmi_calculator.bmi_calculator(height, raw_weight))
    if bmi < 18.5:
        weight_status = 'underweight'
    elif 18.5 <= bmi <= 24.9:
        weight_status = 'normal weight'
    else:
        weight_status = 'overweight/obese'
    ideal_weight = ideal_body_weight.ibw(height, sex)
    adjusted_weight_response = adjusted_body_weight.abw(raw_weight, height, sex)
    serum_creatinine = unit_converter_new.conversion(serum_creatinine_value, 'creatinine', 113.12, None, serum_creatinine_units, 'mg/dL')
    adjusted_weight = 0
    if bmi < 18.5:
        adjusted_weight = weight
    elif 18.5 <= bmi <= 24.9:
        adjusted_weight = min(ideal_weight, weight)
    else:
        adjusted_weight = adjusted_weight_response
    if is_male:
        constant = 1
    else:
        constant = 0.85
    creatinine_clearance = (140 - age) * adjusted_weight * constant / (serum_creatinine * 72)
    return creatinine_clearance
