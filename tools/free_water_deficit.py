import age_conversion
import weight_conversion
import unit_converter_new
from rounding import round_number

def free_water_deficit(age, sex, weight, sodium):
    age = age_conversion.age_conversion(age)
    gender = sex
    if 0 <= age < 18:
        tbw = 0.6
    elif 18 <= age < 65 and gender == 'Male':
        tbw = 0.6
    elif 18 <= age < 65 and gender == 'Female':
        tbw = 0.5
    elif age >= 65 and gender == 'Male':
        tbw = 0.5
    elif age >= 65 and gender == 'Female':
        tbw = 0.45
    weight = weight_conversion.weight_conversion(weight)
    sodium = unit_converter_new.conversion(sodium[0], 'sodium', 22.99, 1, sodium[1], 'mmol/L')
    answer = tbw * weight * (sodium / 140 - 1)
    return answer
