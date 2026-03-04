import delta_gap
import unit_converter_new
from rounding import round_number

def compute_delta_ratio(bicarbonate, sodium, chloride):
    delta_gap_val = delta_gap.compute_delta_gap(sodium, chloride, bicarbonate)
    bicarbonate_val = unit_converter_new.conversion(bicarbonate[0], 'bicarbonate', 61.02, 1, bicarbonate[1], 'mEq/L')
    answer = delta_gap_val / (24 - bicarbonate_val)
    return answer
