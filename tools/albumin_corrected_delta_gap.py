import albumin_corrected_anion
from rounding import round_number

def compute_albumin_corrected_delta_gap(albumin, sodium, chloride, bicarbonate):
    albumin_corrected_resp = albumin_corrected_anion.compute_albumin_corrected_anion(albumin, sodium, chloride, bicarbonate)
    albumin_corrected_val = albumin_corrected_resp
    answer = albumin_corrected_val - 12.0
    return answer
