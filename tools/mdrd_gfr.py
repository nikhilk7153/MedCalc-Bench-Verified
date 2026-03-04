import math
import unit_converter_new
import age_conversion
from rounding import round_number

def mrdr_gfr(sex, age, creatinine, race):
    gender = sex
    age = age_conversion.age_conversion(age)
    creatinine_conc = unit_converter_new.conversion(creatinine[0], 'Creatinine', 113.12, None, creatinine[1], 'mg/dL')
    race_coefficient = 1
    if race is not None:
        race = race
        if race == 'Black':
            race_coefficient = 1.212
    gender_coefficient = 1
    if gender == 'Female':
        gender_coefficient = 0.742
    gfr = 175 * math.exp(math.log(creatinine_conc) * -1.154) * math.exp(math.log(age) * -0.203) * race_coefficient * gender_coefficient
    return gfr
