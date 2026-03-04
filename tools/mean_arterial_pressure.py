from rounding import round_number

def mean_arterial_pressure(sys_bp, dia_bp):
    return sys_bp[0] / 3 + 2 * dia_bp[0] / 3
