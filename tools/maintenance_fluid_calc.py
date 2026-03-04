import weight_conversion
from rounding import round_number

def maintenance_fluid(weight):
    weight = weight_conversion.weight_conversion(weight)
    if weight < 10:
        answer = weight * 4
    elif 10 <= weight <= 20:
        answer = 40 + 2 * (weight - 10)
    elif weight > 20:
        answer = 60 + (weight - 20)
    return answer
