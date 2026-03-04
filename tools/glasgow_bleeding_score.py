import unit_converter_new

def glasgow_bleeding_score(hemoglobin, bun, sex, sys_bp, heart_rate, melena_present=False, syncope=False, hepatic_disease_history=False, cardiac_failure=False):
    score = 0
    hemoglobin = unit_converter_new.conversion(hemoglobin[0], 'hemoglobin', 64500, None, hemoglobin[1], 'g/dL')
    bun = unit_converter_new.conversion(bun[0], 'BUN', 28.08, None, bun[1], 'mg/dL')
    gender = sex
    systolic_bp = sys_bp[0]
    heart_rate = heart_rate[0]
    if gender == 'Male':
        if 12 <= hemoglobin < 13:
            score += 1
        elif 10 <= hemoglobin < 12:
            score += 3
        elif hemoglobin < 10:
            score += 6
    elif 10 <= hemoglobin < 12:
        score += 1
    elif hemoglobin < 10:
        score += 6
    if 18.2 <= bun < 22.4:
        score += 2
    elif 22.4 <= bun < 28:
        score += 3
    elif 28 <= bun <= 70:
        score += 4
    elif bun > 70:
        score += 6
    if 100 <= systolic_bp < 110:
        score += 1
    elif 90 <= systolic_bp < 100:
        score += 2
    elif systolic_bp < 90:
        score += 3
    if heart_rate >= 100:
        score += 1
    score += 1 if melena_present else 0
    score += 2 if syncope else 0
    score += 2 if hepatic_disease_history else 0
    score += 2 if cardiac_failure else 0
    return score
