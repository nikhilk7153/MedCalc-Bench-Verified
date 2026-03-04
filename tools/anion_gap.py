import unit_converter_new
from rounding import round_number

def compute_anion_gap(sodium, chloride, bicarbonate):
    sodium = sodium
    chloride = chloride
    bicarbonate = bicarbonate
    sodium = unit_converter_new.conversion(sodium[0], 'sodium', 22.99, 1, sodium[1], 'mEq/L')
    chloride = unit_converter_new.conversion(chloride[0], 'chloride', 35.45, 1, chloride[1], 'mEq/L')
    bicarbonate = unit_converter_new.conversion(bicarbonate[0], 'bicarbonate', 61.02, 1, bicarbonate[1], 'mEq/L')
    answer = sodium - (chloride + bicarbonate)
    return answer
