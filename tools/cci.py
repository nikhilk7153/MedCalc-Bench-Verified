import age_conversion

def compute_cci(age, mi=False, chf=False, peripheral_vascular_disease=False, cva=False, tia=False, connective_tissue_disease=False, dementia=False, copd=False, hemiplegia=False, peptic_ucler_disease=False, liver_disease='none', diabetes_mellitus='none or diet-controlled', moderate_to_severe_ckd=False, solid_tumor='none', leukemia=False, lymphoma=False, aids=False):
    age_years = age_conversion.age_conversion(age)
    cci = 0
    if 50 <= age_years < 60:
        cci += 1
    elif 60 <= age_years < 70:
        cci += 2
    elif 70 <= age_years < 80:
        cci += 3
    elif age_years >= 80:
        cci += 4
    cci += 1 if mi else 0
    cci += 1 if chf else 0
    cci += 1 if peripheral_vascular_disease else 0
    cci += 1 if cva or tia else 0
    cci += 1 if connective_tissue_disease else 0
    cci += 1 if dementia else 0
    cci += 1 if copd else 0
    cci += 1 if peptic_ucler_disease else 0
    if liver_disease == 'mild':
        cci += 1
    elif liver_disease == 'moderate to severe':
        cci += 3
    if diabetes_mellitus == 'uncomplicated':
        cci += 1
    elif diabetes_mellitus == 'end-organ damage':
        cci += 2
    cci += 2 if hemiplegia else 0
    cci += 2 if moderate_to_severe_ckd else 0
    cci += 2 if leukemia else 0
    cci += 2 if lymphoma else 0
    if solid_tumor == 'localized':
        cci += 2
    elif solid_tumor == 'metastatic':
        cci += 6
    cci += 6 if aids else 0
    return cci
