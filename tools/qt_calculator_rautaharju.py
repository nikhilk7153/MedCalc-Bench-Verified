from rounding import round_number

def rautaharju_calculator(heart_rate, qt_interval):
    heart_rate = heart_rate[0]
    qt_interval = qt_interval[0]
    qt_c = qt_interval * (120 + heart_rate) / 180
    return qt_c
