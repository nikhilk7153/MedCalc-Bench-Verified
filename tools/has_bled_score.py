import age_conversion

def compute_has_bled_score(alcoholic_drinks, age, hypertension=False, liver_disease_has_bled=False, renal_disease_has_bled=False, stroke=False, prior_bleeding=False, labile_inr=False, medications_for_bleeding=False):
    has_bled_score = 0
    num_alcolic_drinks = int(float(alcoholic_drinks))
    age_value = age_conversion.age_conversion(age)
    if age_value > 65:
        has_bled_score += 1
    if num_alcolic_drinks >= 8:
        has_bled_score += 1
    has_bled_score += 1 if hypertension else 0
    has_bled_score += 1 if liver_disease_has_bled else 0
    has_bled_score += 1 if renal_disease_has_bled else 0
    has_bled_score += 1 if stroke else 0
    has_bled_score += 1 if prior_bleeding else 0
    has_bled_score += 1 if labile_inr else 0
    has_bled_score += 1 if medications_for_bleeding else 0
    return has_bled_score
