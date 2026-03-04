import age_conversion

def generate_cha2ds2_vasc(age, sex, chf, hypertension, stroke, tia, thromboembolism, vascular_disease, diabetes):
    score = 0
    age = age_conversion.age_conversion(age)
    if age >= 75:
        score += 2
    elif age >= 65:
        score += 1
    sex = sex
    if sex.lower() == 'female':
        score += 1
    if chf is not None:
        chf = chf
    else:
        chf = False
    if chf:
        score += 1
    if hypertension is not None:
        hypertension = hypertension
    else:
        hypertension = False
    if hypertension:
        score += 1
    if stroke is not None:
        stroke = stroke
    else:
        stroke = False
    if tia is not None:
        tia = tia
    else:
        tia = False
    if thromboembolism is not None:
        thromboembolism = thromboembolism
    else:
        thromboembolism = False
    if stroke or tia or thromboembolism:
        score += 2
    if vascular_disease is not None:
        vascular_disease = vascular_disease
    else:
        vascular_disease = False
    if vascular_disease:
        score += 1
    if diabetes is not None:
        diabetes = diabetes
    else:
        diabetes = False
    if diabetes:
        score += 1
    return score
