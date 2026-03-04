from rounding import round_number

def fahrenheit_to_celsius(temperature, units):
    if units == 'degrees celsius':
        return temperature
    return (temperature - 32) * 5 / 9
