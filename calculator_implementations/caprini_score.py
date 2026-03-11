import age_conversion


param_full_name = { 
                    "surgery_type": "surgery type",
                    "major_surgery_last_month": ("major surgery in the last month", 1),
                    "chf_last_month": ("congestive heart failure in the last month", 1),
                    "sepsis": ("sepsis in the last month", 1),
                    "pneumonia": ("pneumonia in the last month", 1),
                    "immobilizing_plaster_cast": ("immobilizing plaster cast in the last month", 2),
                    "hip_pelvis_leg_fracture": ("hip, pelvis, or leg fracture in the last month", 5),
                    "stroke_last_month": ("stroke in the last month", 5),
                    "multiple_trauma": ("multiple trauma in the last month", 5),
                    "acute_spinal_chord_injury": ("acute spinal cord injury causing paralysis in the last month",  5),
                    "varicose_veins": ("varicose veins", 1),
                    "current_swollen_legs": ("current swollen legs", 1),
                    "current_central_venuous": ("current central venuous access", 2),
                    "previous_dvt": ('previous DVT documented', 3),
                    "previous_pe": ('previous pulmonary embolism documented', 3),
                    "family_history_thrombosis": ("family history of thrombosis", 3),
                    "positive_factor_v": ("Positive Factor V Leiden", 3),
                    "positive_prothrombin": ("Positive prothrombin 20210A", 3),
                    "serum_homocysteine": ("an elevated serum homocysteine", 3),
                    "positive_lupus_anticoagulant": ("a positive lupus anticoagulant", 3),
                    "elevated_anticardiolipin_antibody": ("an elevated anticardiolipin antibody", 3),
                    "heparin_induced_thrombocytopenia": ("a heparin-induced thrombocytopenia", 3),
                    "congenital_acquired_thrombophilia": ("other congenital or acquired thrombophilia", 3),
                    "mobility": "mobility",
                    "inflammatory_bowel_disease": ("history of inflammatory bowel disease", 1),
                    "acute_myocardial_infarction": ("acute Myocardial infarction", 1),
                    "copd": ("chronic Obstructive Pulmonary Disease", 1),
                    "malignancy": ("malignancy", 2),
                    "bmi": "bmi"
                }

surgery_type = {"none": 0, "minor": 1, "major": 2,  "laparoscopic": 2, "arthroscopic": 2, "elective major lower extremity arthroplasty": 5}
mobility = {"normal": 0, "on bed rest": 1, "confined to bed >72 hours": 2}



def caprini_score_explanation(input_parameters):


    explanation = """The criteria for the Caprini Score are listed below:

1. Age, years: ≤40 = 0 points, 41-60 = +1 point, 61-74 = +2 points, ≥75 = +3 points
2. Type of surgery: None = 0 points, Minor = +1 point, Major >45 min (laparoscopic or arthroscopic) = +2 points, Elective major lower extremity arthroplasty = +5 points
3. Recent (≤1 month) event: Major surgery = +1 point, Congestive heart failure (CHF) = +1 point, Sepsis = +1 point, Pneumonia = +1 point, Immobilizing plaster cast = +2 points, Hip, pelvis, or leg fracture = +5 points, Stroke = +5 points, Multiple trauma = +5 points, Acute spinal cord injury causing paralysis = +5 points
4. Venous disease or clotting disorder: Varicose veins = +1 point, Current swollen legs = +1 point, Current central venous access = +2 points, History of deep vein thrombosis (DVT) or pulmonary embolism (PE) = +3 points, Family history of thrombosis = +3 points, Positive Factor V Leiden = +3 points, Positive prothrombin 20210A = +3 points, 
    Elevated serum homocysteine = +3 points, Positive lupus anticoagulant = +3 points, Elevated anticardiolipin antibody = +3 points, Heparin-induced thrombocytopenia = +3 points, Other congenital or acquired thrombophilia = +3 points
5. Mobility: Normal, out of bed = 0 points, Medical patient currently on bed rest = +1 point, Patient confined to bed >72 hours = +2 points
6. Other present and past history: History of inflammatory bowel disease = +1 point, BMI > 25 = +1 point, Acute myocardial infarction = +1 point, Chronic obstructive pulmonary disease (COPD) = +1 point, Present or previous malignancy = +2 points

The total Caprini Score is calculated by summing the points for each criterion.
"""


    explanation += "\nThe patient's current caprini score is 0.\n"
    score = 0

    gender = input_parameters["sex"]

    explanation += f"The patient's gender is {gender}.\n"

    age_exp, age = age_conversion.age_conversion_explanation(input_parameters["age"])
    explanation += age_exp

    if age <= 40:
        explanation += f"Because the patient's age is less or equal to 40, we do not add any points to the total, keeping the current total at {score}.\n"
    elif 41 <= age <= 60:
        explanation += f"Because the patient's age is between 41 and 60, we add one point to the current total, making the current total, {score} + 1 = {score + 1}.\n"
        score += 1
    elif 61 <= age <= 74:
        explanation += f"Because the patient's age is between 61 and 74, we add two points to the current total, making the current total, {score} + 2 = {score + 2}.\n"
        score += 2
    elif age >= 75:
        explanation += f"Because the patient's age at least 75, we add three points to the current total, making the current total, {score} + 3 = {score + 3}.\n"
        score += 3


    for param, value in param_full_name.items():
        
        if param not in input_parameters:
            explanation += f"The patient does not report anything about {param_full_name[param][0]} and so we assume this to be false. Hence, 0 points are added to the score, keeping the total at {score}. "

        elif param == "mobility":
            value = input_parameters[param]

            explanation += f"The patient's mobility status is determined to be '{value}'. Hence, we add {mobility[value]} points to the total, making the current total {mobility[value]} + {score} = {mobility[value] + score}.\n "
            score += mobility[value]

        elif param == "surgery_type":
            value = input_parameters[param]
            explanation += f"The patient's surgery type is determined to be '{value}'. Hence, we add {surgery_type[value]} points to the total, making the current total {surgery_type[value]} + {score} = {surgery_type[value] + score}.\n "
            score += surgery_type[value]

        elif param == "bmi":
        
            if input_parameters["bmi"][0] > 25:
                explanation += f"The patient's BMI is {input_parameters['bmi'][0]} kg/m^2, which is greater than 25 kg/m^2, and so we add 1 point to the total, making the current total {score} + 1 = {score + 1}.\n"
                score += 1
            else:
                explanation += f"The patient's BMI is {input_parameters['bmi'][0]} kg/m^2, which is less than 25 kg/m^2, and so we add 0 points to the total, keeping the total at {score}.\n"

        elif input_parameters[param]:
            points = param_full_name[param][1]
            explanation += f"The patient's has {param_full_name[param][0]}. Hence, we add {points} to the total, making the current total {points} + {score} = {points + score}.\n "
            score += points

        elif not input_parameters[param]:
            points = param_full_name[param][1]
            explanation += f"The patient's has does not have {param_full_name[param][0]}. Hence, 0 points are added to the score, keeping the total at {score}."
    

    explanation += f"The final caprini score is {score}."
    return {"Explanation": explanation, "Answer": score}


def caprini_score(
    sex,
    age,
    bmi=None,
    surgery_type_value=None,
    mobility_value=None,
    major_surgery_last_month=False,
    chf_last_month=False,
    sepsis=False,
    pneumonia=False,
    immobilizing_plaster_cast=False,
    hip_pelvis_leg_fracture=False,
    stroke_last_month=False,
    multiple_trauma=False,
    acute_spinal_chord_injury=False,
    varicose_veins=False,
    current_swollen_legs=False,
    current_central_venuous=False,
    previous_dvt=False,
    previous_pe=False,
    family_history_thrombosis=False,
    positive_factor_v=False,
    positive_prothrombin=False,
    serum_homocysteine=False,
    positive_lupus_anticoagulant=False,
    elevated_anticardiolipin_antibody=False,
    heparin_induced_thrombocytopenia=False,
    congenital_acquired_thrombophilia=False,
    inflammatory_bowel_disease=False,
    acute_myocardial_infarction=False,
    copd=False,
    malignancy=False,
):
    score = 0
    age = age_conversion.age_conversion(age)
    if age <= 40:
        pass
    elif 41 <= age <= 60:
        score += 1
    elif 61 <= age <= 74:
        score += 2
    elif age >= 75:
        score += 3
    if mobility_value is not None:
        score += mobility.get(str(mobility_value).lower(), 0)
    if surgery_type_value is not None:
        score += surgery_type.get(str(surgery_type_value).lower(), 0)
    if bmi is not None:
        bmi_value = bmi[0] if isinstance(bmi, (list, tuple)) else bmi
        if bmi_value > 25:
            score += 1

    score += 1 if major_surgery_last_month else 0
    score += 1 if chf_last_month else 0
    score += 1 if sepsis else 0
    score += 1 if pneumonia else 0
    score += 2 if immobilizing_plaster_cast else 0
    score += 5 if hip_pelvis_leg_fracture else 0
    score += 5 if stroke_last_month else 0
    score += 5 if multiple_trauma else 0
    score += 5 if acute_spinal_chord_injury else 0
    score += 1 if varicose_veins else 0
    score += 1 if current_swollen_legs else 0
    score += 2 if current_central_venuous else 0
    score += 3 if previous_dvt else 0
    score += 3 if previous_pe else 0
    score += 3 if family_history_thrombosis else 0
    score += 3 if positive_factor_v else 0
    score += 3 if positive_prothrombin else 0
    score += 3 if serum_homocysteine else 0
    score += 3 if positive_lupus_anticoagulant else 0
    score += 3 if elevated_anticardiolipin_antibody else 0
    score += 3 if heparin_induced_thrombocytopenia else 0
    score += 3 if congenital_acquired_thrombophilia else 0
    score += 1 if inflammatory_bowel_disease else 0
    score += 1 if acute_myocardial_infarction else 0
    score += 1 if copd else 0
    score += 2 if malignancy else 0
    return score


