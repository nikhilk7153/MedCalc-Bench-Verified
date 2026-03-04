import height_conversion
import weight_conversion


def bmi_calculator(height, weight):
    height = height_conversion.height_conversion(height)
    weight = weight_conversion.weight_conversion(weight)
    result = weight / (height * height)
    return result
