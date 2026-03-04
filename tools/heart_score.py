import age_conversion

def compute_heart_score(age, history='Slightly suspicious', electrocardiogram='Normal', initial_troponin='less than or equal to normal limit', hypertension=False, hypercholesterolemia=False, diabetes_mellitus=False, obesity=False, smoking=False, family_with_cvd=False, atherosclerotic_disease=False):
    total_score = 0
    history_points = {'Slightly suspicious': 0, 'Moderately suspicious': 1, 'Highly suspicious': 2}
    ekg_points = {'Normal': 0, 'Non-specific repolarization disturbance': 1, 'Significant ST deviation': 2}
    troponin_points = {'less than or equal to normal limit': 0, 'between the normal limit or up to three times the normal limit': 1, 'greater than three times normal limit': 2}
    total_score += history_points[history]
    total_score += ekg_points[electrocardiogram]
    total_score += troponin_points[initial_troponin]
    age_years = age_conversion.age_conversion(age)
    if 45 <= age_years < 65:
        total_score += 1
    elif age_years >= 65:
        total_score += 2
    risk_count = sum([hypertension, hypercholesterolemia, diabetes_mellitus, obesity, smoking, family_with_cvd, atherosclerotic_disease])
    if atherosclerotic_disease:
        total_score += 2
    elif 1 <= risk_count <= 2:
        total_score += 1
    elif risk_count >= 3:
        total_score += 2
    return total_score
