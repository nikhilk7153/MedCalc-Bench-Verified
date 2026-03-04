import convert_temperature
import age_conversion

def compute_centor_score(age, temperature, cough_absent=None, tender_lymph_nodes=False, exudate_swelling_tonsils=False):
    centor_score = 0
    age = age_conversion.age_conversion(age)
    if 3 <= age <= 14:
        centor_score += 1
    elif 15 <= age <= 44:
        pass
    elif age >= 45:
        centor_score -= 1
    temp_val = convert_temperature.fahrenheit_to_celsius(temperature[0], temperature[1])
    if temp_val > 38:
        centor_score += 1
    if cough_absent is None or cough_absent:
        centor_score += 1
    if tender_lymph_nodes:
        centor_score += 1
    if exudate_swelling_tonsils:
        centor_score += 1
    return centor_score
