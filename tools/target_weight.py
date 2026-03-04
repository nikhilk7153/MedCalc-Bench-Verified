import json
import height_conversion
from rounding import round_number

def targetweight(body_mass_index, height):
    bmi = body_mass_index[0]
    height = height_conversion.height_conversion(height)
    target_weight_val = bmi * (height * height)
    return target_weight_val
