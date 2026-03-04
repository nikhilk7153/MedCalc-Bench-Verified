import unit_converter_new
import convert_temperature
import age_conversion
import mean_arterial_pressure

def apache_ii(sodium, pH, heart_rate, respiratory_rate, potassium, creatinine, hematocrit, wbc, fio2, gcs, a_a_gradient=None, pao2=None, age=None, organ_failure_or_immunocompromise=False, temperature=None, acute_renal_failure=None, chronic_renal_failure=None, surgery_type=None, sys_bp=None, dia_bp=None):
    score = 0
    sodium = unit_converter_new.conversion(sodium[0], 'sodium', 22.99, 1, sodium[1], 'mmol/L')
    pH = pH
    heart_rate = heart_rate[0]
    respiratory_rate = respiratory_rate[0]
    potassium = unit_converter_new.conversion(potassium[0], 'potassium', 39.1, 1, potassium[1], 'mmol/L')
    creatinine = unit_converter_new.conversion(creatinine[0], 'creatinine', 113.12, None, creatinine[1], 'mg/dL')
    acute_renal_failure = acute_renal_failure if acute_renal_failure is not None else False
    chronic_renal_failure = chronic_renal_failure if chronic_renal_failure is not None else False
    hematocrit = hematocrit[0]
    wbc = unit_converter_new.convert_to_units_per_liter(wbc[0], wbc[1], 'white blood cell count', 'L')
    fio2 = fio2[0]
    gcs = int(gcs)
    a_a_gradient = a_a_gradient if a_a_gradient is not None else False
    partial_pressure_oxygen = pao2 if pao2 is not None else False
    age = age_conversion.age_conversion(age)
    if age < 45:
        pass
    elif 45 <= age <= 54:
        score += 2
    elif 55 <= age <= 64:
        score += 3
    elif 65 <= age <= 74:
        score += 5
    elif age >= 75:
        score += 6
    if organ_failure_or_immunocompromise is not None:
        if organ_failure_or_immunocompromise:
            surgery_type = surgery_type if surgery_type is not None else None
            if surgery_type in ('Nonoperative', 'Emergency'):
                score += 5
            elif surgery_type == 'Elective':
                score += 2
    if fio2 >= 50:
        a_a_gradient = a_a_gradient
        if a_a_gradient > 499:
            score += 4
        elif 350 <= a_a_gradient <= 499:
            score += 3
        elif 200 <= a_a_gradient <= 349:
            score += 2
    else:
        partial_pressure_oxygen = pao2[0]
        if partial_pressure_oxygen > 70:
            pass
        elif 61 <= partial_pressure_oxygen <= 70:
            score += 1
        elif 55 <= partial_pressure_oxygen <= 60:
            score += 3
        else:
            score += 4
    temperature = convert_temperature.fahrenheit_to_celsius(temperature[0], temperature[1])
    if temperature >= 41:
        score += 4
    elif 39 <= temperature < 41:
        score += 3
    elif 38.5 <= temperature < 39:
        score += 1
    elif 36 <= temperature < 38.5:
        pass
    elif 34 <= temperature < 36:
        score += 1
    elif 32 <= temperature < 34:
        score += 2
    elif 30 <= temperature < 32:
        score += 3
    elif temperature < 30:
        score += 4
    if sys_bp is not None and dia_bp is not None:
        map_value = mean_arterial_pressure.mean_arterial_pressure(sys_bp, dia_bp)
    else:
        map_value = 0
    if map_value > 159:
        score += 4
    elif 129 < map_value <= 159:
        score += 3
    elif 109 < map_value <= 129:
        score += 2
    elif 69 < map_value <= 109:
        pass
    elif 49 < map_value <= 69:
        score += 2
    elif map_value <= 49:
        score += 4
    if heart_rate >= 180:
        score += 4
    elif 140 <= heart_rate < 180:
        score += 3
    elif 110 <= heart_rate < 140:
        score += 2
    elif 70 <= heart_rate < 110:
        pass
    elif 55 <= heart_rate < 70:
        score += 2
    elif 40 <= heart_rate < 55:
        score += 3
    elif heart_rate < 40:
        score += 4
    if respiratory_rate >= 50:
        score += 4
    elif 35 <= respiratory_rate < 50:
        score += 3
    elif 25 <= respiratory_rate < 35:
        score += 1
    elif 12 <= respiratory_rate < 25:
        pass
    elif 10 <= respiratory_rate < 12:
        score += 1
    elif 6 <= respiratory_rate < 10:
        score += 2
    elif respiratory_rate < 6:
        score += 4
    if pH >= 7.7:
        score += 4
    elif 7.6 <= pH < 7.7:
        score += 3
    elif 7.5 <= pH < 7.6:
        score += 1
    elif 7.33 <= pH < 7.5:
        pass
    elif 7.25 <= pH < 7.33:
        score += 2
    elif 7.15 <= pH < 7.25:
        score += 3
    elif pH < 7.15:
        score += 4
    if sodium >= 180:
        score += 4
    elif 160 <= sodium < 180:
        score += 3
    elif 155 <= sodium < 160:
        score += 2
    elif 150 <= sodium < 155:
        score += 1
    elif 130 <= sodium < 150:
        pass
    elif 120 <= sodium < 130:
        score += 2
    elif 111 <= sodium < 120:
        score += 3
    elif sodium < 111:
        score += 4
    if potassium >= 7.0:
        score += 4
    elif 6.0 <= potassium < 7.0:
        score += 3
    elif 5.5 <= potassium < 6.0:
        score += 1
    elif 3.5 <= potassium < 5.5:
        pass
    elif 3.0 <= potassium < 3.5:
        score += 1
    elif 2.5 <= potassium < 3.0:
        score += 2
    elif potassium < 2.5:
        score += 4
    if creatinine >= 3.5 and acute_renal_failure:
        additional_points = 8
        score += additional_points
    elif 2.0 <= creatinine < 3.5 and acute_renal_failure:
        additional_points = 6
        score += additional_points
    elif creatinine >= 3.5 and chronic_renal_failure:
        additional_points = 4
        score += additional_points
    elif 2.0 <= creatinine < 3.5 and chronic_renal_failure:
        additional_points = 3
        score += additional_points
    elif 1.5 <= creatinine < 2.0 and acute_renal_failure:
        additional_points = 4
        score += additional_points
    elif 1.5 <= creatinine < 2.0 and chronic_renal_failure:
        additional_points = 2
        score += additional_points
    if not acute_renal_failure and (not chronic_renal_failure):
        if creatinine >= 3.5:
            additional_points = 4
            score += additional_points
        elif 2.0 <= creatinine < 3.5:
            additional_points = 3
            score += additional_points
        elif 1.5 <= creatinine < 2.0:
            additional_points = 2
            score += additional_points
        elif 0.6 <= creatinine < 1.5:
            pass
        elif creatinine < 0.6:
            additional_points = 2
            score += additional_points
    if hematocrit >= 60:
        score += 4
    elif 50 <= hematocrit < 60:
        score += 2
    elif 46 <= hematocrit < 50:
        score += 1
    elif 30 <= hematocrit < 46:
        pass
    elif 20 <= hematocrit < 30:
        score += 2
    elif hematocrit < 20:
        score += 4
    if wbc >= 40000000000.0:
        score += 4
    elif 20000000000.0 <= wbc < 40000000000.0:
        score += 2
    elif 15000000000.0 <= wbc < 20000000000.0:
        score += 1
    elif 3000000000.0 <= wbc < 15000000000.0:
        pass
    elif 1000000000.0 <= wbc < 3000000000.0:
        score += 2
    elif wbc < 1000000000.0:
        score += 4
    gcs = int(gcs)
    apache_ii_gcs = int(15 - gcs)
    score += apache_ii_gcs
    return score
