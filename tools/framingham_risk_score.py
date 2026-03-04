import unit_converter_new
import age_conversion
import math
from rounding import round_number

def framingham_risk_score(age, sex, smoker, bp_medicine, total_cholesterol, hdl_cholesterol, sys_bp):
    age = age
    gender = sex
    age = age_conversion.age_conversion(age)
    age_smoke = min(age, 70 if gender == 'Male' else 78)
    if smoker is None:
        smoker = 0
    else:
        smoker = 1 if smoker else 0
    if bp_medicine is None:
        bp_medicine = 0
    else:
        bp_medicine = 1 if bp_medicine else 0
    total_cholesterol = total_cholesterol
    hdl_cholesterol = hdl_cholesterol
    sys_bp = sys_bp[0]
    total_cholesterol = unit_converter_new.conversion(total_cholesterol[0], 'total cholesterol', 386.654, None, total_cholesterol[1], 'mg/dL')
    hdl_cholesterol = unit_converter_new.conversion(hdl_cholesterol[0], 'hdl cholesterol', 386.654, None, hdl_cholesterol[1], 'mg/dL')
    ln_age = math.log(age)
    ln_total_cholesterol = math.log(total_cholesterol)
    ln_hdl_cholesterol = math.log(hdl_cholesterol)
    ln_sys_bp = math.log(sys_bp)
    ln_age_smoke = math.log(age_smoke)
    coefficients = {'Male': {'ln_age': 52.00961, 'ln_total_cholesterol': 20.014077, 'ln_hdl_cholesterol': -0.905964, 'ln_sys_bp': 1.305784, 'bp_medicine': 0.241549, 'smoker': 12.096316, 'ln_age_ln_total_cholesterol': -4.605038, 'ln_age_smoker': -2.84367, 'ln_age_ln_age': -2.93323, 'constant': -172.300168}, 'Female': {'ln_age': 31.764001, 'ln_total_cholesterol': 22.465206, 'ln_hdl_cholesterol': -1.187731, 'ln_sys_bp': 2.552905, 'bp_medicine': 0.420251, 'smoker': 13.07543, 'ln_age_ln_total_cholesterol': -5.060998, 'ln_age_smoker': -2.996945, 'ln_age_ln_age': 0, 'constant': -146.5933061}}
    beta = coefficients[gender]
    risk_score = beta['ln_age'] * ln_age + beta['ln_total_cholesterol'] * ln_total_cholesterol + beta['ln_hdl_cholesterol'] * ln_hdl_cholesterol + beta['ln_sys_bp'] * ln_sys_bp + beta['bp_medicine'] * bp_medicine + beta['smoker'] * smoker + beta['ln_age_ln_total_cholesterol'] * ln_age * ln_total_cholesterol + beta['ln_age_smoker'] * ln_age_smoke * smoker + beta['ln_age_ln_age'] * ln_age * ln_age + beta['constant']
    if gender == 'Male':
        risk_percentage = 1 - 0.9402 ** math.exp(risk_score)
    else:
        risk_percentage = 1 - 0.98767 ** math.exp(risk_score)
    risk_percentage *= 100
    return round(risk_percentage, 3)
