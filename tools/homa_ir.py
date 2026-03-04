import unit_converter_new
from rounding import round_number

def compute_homa_ir(insulin, glucose):
    insulin_value = insulin[0]
    insulin_unit = insulin[1]
    if insulin_unit == 'µIU/mL':
        pass
    elif insulin_unit == 'pmol/L':
        insulin_value = insulin_value * 6
    elif insulin_unit == 'ng/mL':
        insulin_value = insulin_value * 24.8
    glucose = unit_converter_new.conversion(glucose[0], 'glucose', 180.16, None, glucose[1], 'mg/dL')
    answer = insulin_value * glucose / 405
    return answer
