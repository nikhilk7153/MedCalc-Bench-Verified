import unit_converter_new
import convert_temperature

def sirs_criteria(temperature, heart_rate, wbc, respiratory_rate, paco2=None):
    temperature = temperature
    temperature = convert_temperature.fahrenheit_to_celsius(temperature[0], temperature[1])
    heart_rate = heart_rate[0]
    wbc = unit_converter_new.convert_to_units_per_liter(wbc[0], wbc[1], 'white blood cell', 'mm^3')
    criteria_met = 0
    if temperature > 38:
        criteria_met += 1
    elif temperature < 36:
        criteria_met += 1
    if heart_rate > 90:
        criteria_met += 1
    if wbc > 12000:
        criteria_met += 1
    elif wbc < 4000:
        criteria_met += 1
    if respiratory_rate is not None:
        respiratory_rate = respiratory_rate[0]
        res = ''
        if respiratory_rate > 20:
            res += f'which is greater than 20 breaths per minute. '
            resp_met = True
        else:
            res += 'which is less or equal to than 20 breaths per min. '
            resp_met = False
    else:
        resp_met = False
    if paco2 is not None:
        paco2 = paco2[0]
        res = ''
        if paco2 < 32:
            res += f'which is less than than 32 mm Hg. '
            paco2_met = True
        elif paco2 > 32:
            res += f'which is greater or equal to than 32 mm Hg. '
            paco2_met = False
    else:
        paco2_met = False
    if resp_met or paco2_met:
        criteria_met += 1
    return criteria_met
