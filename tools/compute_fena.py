import unit_converter_new
from rounding import round_number

def compute_fena(sodium, creatinine, urine_sodium, urine_creatinine):
    sodium = unit_converter_new.conversion(sodium[0], 'sodium', 22.99, 1, sodium[1], 'mEq/L')
    creatinine = unit_converter_new.conversion(creatinine[0], 'creatinine', 113.12, 1, creatinine[1], 'mg/dL')
    urine_sodium = unit_converter_new.conversion(urine_sodium[0], 'urine sodium', 22.99, 1, urine_sodium[1], 'mEq/L')
    urine_creatinine = unit_converter_new.conversion(urine_creatinine[0], 'urine creatinine', 113.12, 1, urine_creatinine[1], 'mg/dL')
    result = creatinine * urine_sodium / (sodium * urine_creatinine) * 100
    return result
