import math
import unit_converter_new
from rounding import round_number

def compute_meldna(creatinine, dialysis_twice, cvvhd, bilirubin, inr, sodium):
    meldna = 0
    creatinine = unit_converter_new.conversion(creatinine[0], 'creatinine', 113.12, None, creatinine[1], 'mg/dL')
    if dialysis_twice is None:
        dialysis_twice = False
    if cvvhd is None:
        cvvhd = False
    if creatinine < 1.0:
        creatinine = 1.0
    elif creatinine > 4.0:
        creatinine = 4.0
    elif dialysis_twice or cvvhd:
        creatinine = 4.0
    bilirubin = unit_converter_new.conversion(bilirubin[0], 'bilirubin', None, None, bilirubin[1], 'mg/dL')
    if bilirubin < 1.0:
        bilirubin = 1.0
    inr = inr
    if inr < 1.0:
        inr = 1.0
    sodium = unit_converter_new.conversion(sodium[0], 'sodium', 22.99, 1, sodium[1], 'mEq/L')
    if sodium < 125:
        sodium = 125
    elif sodium > 137:
        sodium = 137
    meld_i = 0.957 * math.log(creatinine) + 0.378 * math.log(bilirubin) + 1.12 * math.log(inr) + 0.643
    meld_i_rounded = round(meld_i, 1)
    meld_10 = round(meld_i_rounded * 10)
    meld = round(meld_10 + 1.32 * (137 - sodium) - 0.033 * meld_10 * (137 - sodium))
    if meld_10 > 11:
        if meld > 40:
            meldna = 40
        else:
            meldna = meld
    else:
        meldna = meld_10
    return round(meldna)
