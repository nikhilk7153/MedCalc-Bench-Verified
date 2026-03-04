import math
import height_conversion
import weight_conversion


def bsa_calculator(height, weight):
    height = height_conversion.height_conversion_cm(height)
    weight = weight_conversion.weight_conversion(weight)
    return math.sqrt(weight * height / 3600)
