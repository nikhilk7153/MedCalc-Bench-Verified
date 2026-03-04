import weight_conversion
import ideal_body_weight
from rounding import round_number

def abw(weight, height, sex):
    weight = weight_conversion.weight_conversion(weight)
    ibw = ideal_body_weight.ibw(height, sex)
    abw = ibw + 0.4 * (weight - ibw)
    return abw
