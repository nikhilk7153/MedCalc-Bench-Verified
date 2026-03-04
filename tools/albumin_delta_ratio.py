import unit_converter_new
import albumin_corrected_delta_gap


def compute_albumin_delta_ratio(bicarbonate, albumin, sodium, chloride):
    albumin_delta_gap_val = albumin_corrected_delta_gap.compute_albumin_corrected_delta_gap(albumin, sodium, chloride, bicarbonate)
    bicarbonate_val = unit_converter_new.conversion(bicarbonate[0], 'bicarbonate', 61.02, 1, bicarbonate[1], 'mEq/L')
    final_answer = albumin_delta_gap_val / (24 - bicarbonate_val)
    return final_answer
