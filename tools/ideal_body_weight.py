import height_conversion
from rounding import round_number

def ibw(height, sex):
    height = height
    gender = sex
    height = height_conversion.height_conversion_in(height)
    if gender == 'Male':
        ibw = 50 + 2.3 * (height - 60)
    elif gender == 'Female':
        ibw = 45.5 + 2.3 * (height - 60)
    return ibw
