from rounding import round_number

def fredericia_calculator(heart_rate, qt_interval):
    heart_rate = heart_rate[0]
    qt_interval = qt_interval[0]
    rr_interval_sec = 60 / heart_rate
    qt_c = qt_interval / rr_interval_sec ** (1 / 3)
    return qt_c
