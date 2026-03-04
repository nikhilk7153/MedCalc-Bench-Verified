import age_conversion
import unit_converter_new

def curb_65(bun, respiratory_rate, sys_bp, dia_bp, age, confusion):
    curb_65_score = 0
    bun = unit_converter_new.conversion(bun[0], 'BUN', 28.02, None, bun[1], 'mg/dL')
    respiratory_rate = int(respiratory_rate[0])
    sys_bp = int(sys_bp[0])
    dia_bp = int(dia_bp[0])
    age = age_conversion.age_conversion(age)
    if age >= 65:
        curb_65_score += 1
    if confusion is None:
        pass
    elif confusion:
        curb_65_score += 1
    if bun > 19:
        curb_65_score += 1
    if respiratory_rate >= 30:
        curb_65_score += 1
    if sys_bp < 90 or dia_bp <= 60:
        curb_65_score += 1
    return curb_65_score
