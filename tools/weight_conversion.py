from rounding import round_number

def weight_conversion(weight_info):
    weight = weight_info[0]
    weight_label = weight_info[1]
    if weight_label == 'lbs':
        return weight * 0.453592
    if weight_label == 'g':
        return weight / 1000
    return weight
