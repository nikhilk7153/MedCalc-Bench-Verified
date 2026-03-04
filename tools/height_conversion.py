from rounding import round_number

def height_conversion(height_info):
    if len(height_info) == 4:
        inches = height_info[0] * 12 + height_info[2]
        return inches * 0.0254
    if height_info[-1] == 'm':
        return height_info[0]
    if height_info[-1] == 'cm':
        return height_info[0] / 100
    if height_info[-1] == 'ft':
        return height_info[0] * 0.3048
    if height_info[-1] == 'in':
        return height_info[0] * 0.0254

def height_conversion_explanation_cm(height_info):
    if len(height_info) == 4:
        feet = height_info[0]
        inches = height_info[2]
        total_inches = feet * 12 + inches
        centimeters = round_number(total_inches * 2.54)
        explanation = f"The patient's height is {feet} ft {inches} in which converts to {feet} ft * 12 in/ft + {inches} in = {total_inches} in. Hence, the patient's height is {total_inches} in * 2.54 cm/in = {centimeters} cm. "
        return (explanation, centimeters)
    elif height_info[-1] == 'm':
        height_meters = height_info[0]
        centimeters = round_number(height_meters * 100)
        explanation = f"The patient's height is {height_meters} m, which is {height_meters} m * 100 cm/m = {centimeters} cm. "
        return (explanation, centimeters)
    elif height_info[-1] == 'cm':
        height_cm = height_info[0]
        explanation = f"The patient's height is {height_cm} cm. "
        return (explanation, height_cm)
    elif height_info[-1] == 'ft':
        height_ft = height_info[0]
        centimeters = round_number(height_ft * 30.48)
        explanation = f"The patient's height is {height_ft} ft, which is {height_ft} ft * 30.48 cm/ft = {centimeters} cm. "
        return (explanation, centimeters)
    elif height_info[-1] == 'in':
        height_in = height_info[0]
        centimeters = round_number(height_in * 2.54)
        explanation = f"The patient's height is {height_in} in, which is {height_in} in * 2.54 cm/in = {centimeters} cm. "
        return (explanation, centimeters)

def height_conversion_cm(height_info):
    if len(height_info) == 4:
        feet = height_info[0]
        inches = height_info[2]
        total_inches = feet * 12 + inches
        return total_inches * 2.54
    if height_info[-1] == 'm':
        return height_info[0] * 100
    if height_info[-1] == 'cm':
        return height_info[0]
    if height_info[-1] == 'ft':
        return height_info[0] * 30.48
    if height_info[-1] == 'in':
        return height_info[0] * 2.54

def height_conversion_explanation_in(height_info):
    if len(height_info) == 4:
        feet = height_info[0]
        inches = height_info[2]
        total_inches = round_number(feet * 12 + inches)
        explanation = f"The patient's height is {feet} ft {inches} in which converts to {feet} ft * 12 in/ft + {inches} in = {total_inches} in. Hence, the patient's height is {total_inches} in. "
        return (explanation, total_inches)
    elif height_info[-1] == 'm':
        height_meters = height_info[0]
        inches = round_number(height_meters * 39.3701)
        explanation = f"The patient's height is {height_meters} m, which is {height_meters} m * 39.3701 in/m = {inches} in. "
        return (explanation, inches)
    elif height_info[-1] == 'cm':
        height_cm = height_info[0]
        inches = round_number(height_cm * 0.393701)
        explanation = f"The patient's height is {height_cm} cm, which is {height_cm} cm * 0.393701 in/cm = {inches} in. "
        return (explanation, inches)
    elif height_info[-1] == 'ft':
        height_ft = height_info[0]
        inches = round_number(height_ft * 12)
        explanation = f"The patient's height is {height_ft} ft, which is {height_ft} ft * 12 in/ft = {inches} in. "
        return (explanation, inches)
    elif height_info[-1] == 'in':
        height_in = height_info[0]
        explanation = f"The patient's height is {height_in} in. "
        return (explanation, height_in)

def height_conversion_in(height_info):
    if len(height_info) == 4:
        feet = height_info[0]
        inches = height_info[2]
        return feet * 12 + inches
    if height_info[-1] == 'm':
        return height_info[0] * 39.3701
    if height_info[-1] == 'cm':
        return height_info[0] * 0.393701
    if height_info[-1] == 'ft':
        return height_info[0] * 12
    if height_info[-1] == 'in':
        return height_info[0]
