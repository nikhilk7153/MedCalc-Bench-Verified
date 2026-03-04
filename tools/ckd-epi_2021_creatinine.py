import age_conversion
import unit_converter_new
from rounding import round_number

def ckd_epi_2021(age, sex, creatinine):
    age = age_conversion.age_conversion(age)
    gender = sex
    if gender == 'Female':
        gender_coefficient = 1.012
    else:
        gender_coefficient = 1.0
    creatinine_val, creatinine_label = (creatinine[0], creatinine[1])
    creatinine_val = unit_converter_new.conversion(creatinine_val, 'Serum Creatinine', 113.12, None, creatinine_label, 'mg/dL')
    if creatinine_val <= 0.7 and gender == 'Female':
        a = 0.7
        b = -0.241
    elif creatinine_val <= 0.9 and gender == 'Male':
        a = 0.9
        b = -0.302
    elif creatinine_val > 0.7 and gender == 'Female':
        a = 0.7
        b = -1.2
    elif creatinine_val > 0.9 and gender == 'Male':
        a = 0.9
        b = -1.2
    result = 142 * (creatinine_val / a) ** b * 0.9938 ** age * gender_coefficient
    return result
