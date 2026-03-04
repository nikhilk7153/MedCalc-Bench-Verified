import unit_converter_new
from rounding import round_number

def compute_serum_osmolality(sodium, bun, glucose):
    sodium = unit_converter_new.conversion(sodium[0], 'sodium', 22.99, 1, sodium[1], 'mmol/L')
    bun = unit_converter_new.conversion(bun[0], 'bun', 28.02, None, bun[1], 'mg/dL')
    glucose = unit_converter_new.conversion(glucose[0], 'glucose', 180.16, None, glucose[1], 'mg/dL')
    serum_os = 2 * sodium + bun / 2.8 + glucose / 18
    return serum_os
