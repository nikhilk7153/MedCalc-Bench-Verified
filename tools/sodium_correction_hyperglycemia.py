import unit_converter_new
from rounding import round_number

def compute_sodium_correction_hyperglycemia(sodium, glucose):
    sodium = sodium
    glucose = glucose
    sodium = unit_converter_new.conversion(sodium[0], 'sodium', 22.99, 1, sodium[1], 'mEq/L')
    glucose = unit_converter_new.conversion(glucose[0], 'glucose', 180.16, None, glucose[1], 'mg/dL')
    corrected_sodium = sodium + 0.024 * (glucose - 100)
    return corrected_sodium
