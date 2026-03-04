import anion_gap
import unit_converter_new


def compute_albumin_corrected_anion(albumin, sodium, chloride, bicarbonate):
    anion_gap_data = anion_gap.compute_anion_gap(sodium, chloride, bicarbonate)
    albumin = unit_converter_new.conversion(albumin[0], 'albumin', None, None, albumin[1], 'g/dL')
    anion_gap_val = anion_gap_data
    answer = anion_gap_val + 2.5 * (4 - albumin)
    final_answer = answer
    return final_answer
