import anion_gap
from rounding import round_number

def compute_delta_gap(sodium, chloride, bicarbonate):
    anion_gap_val = anion_gap.compute_anion_gap(sodium, chloride, bicarbonate)
    answer = anion_gap_val - 12.0
    return answer
