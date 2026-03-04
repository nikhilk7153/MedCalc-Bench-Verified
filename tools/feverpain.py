def compute_fever_pain(fever_24_hours=False, cough_coryza_absent=None, symptom_onset=False, purulent_tonsils=False, severe_tonsil_inflammation=False):
    fever_pain_score = 0
    if fever_24_hours:
        fever_pain_score += 1
    if cough_coryza_absent is None or cough_coryza_absent:
        fever_pain_score += 1
    if symptom_onset:
        fever_pain_score += 1
    if purulent_tonsils:
        fever_pain_score += 1
    if severe_tonsil_inflammation:
        fever_pain_score += 1
    return fever_pain_score
