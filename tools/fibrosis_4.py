import math
import unit_converter_new
import age_conversion
from rounding import round_number

def compute_fib4(age, ast, alt, platelet_count):
    age = age_conversion.age_conversion(age)
    ast_value = ast[0]
    alt_value = alt[0]
    src_value = platelet_count[0]
    src_unit = platelet_count[1]
    platelet_value = unit_converter_new.convert_to_units_per_liter(src_value, src_unit, 'platelets', 'L')
    count_platelet_billions = platelet_value / 1000000000.0
    result = age * ast_value / (count_platelet_billions * math.sqrt(alt_value))
    return result
