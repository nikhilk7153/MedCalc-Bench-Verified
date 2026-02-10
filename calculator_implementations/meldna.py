import math
import unit_converter_new
import age_conversion

def round_half_up(value):
    if value >= 0:
        return int(math.floor(value + 0.5))
    return int(math.ceil(value - 0.5))

def compute_meldna_explanation(input_variables):
    
    meldna = 0

    explanation = (
        "The OPTN MELD 3.0 calculation uses natural logs and capped lab values.\n"
        "For candidates who are at least 18 years old at registration:\n"
        "MELD = 1.33 (if female) + [4.56 x ln(bilirubin)] + [0.82 x (137 - sodium)] - "
        "[0.24 x (137 - sodium) x ln(bilirubin)] + [9.09 x ln(INR)] + [11.14 x ln(creatinine)] + "
        "[1.85 x (3.5 - albumin)] - [1.83 x (3.5 - albumin) x ln(creatinine)] + 6.\n"
        "For candidates 12-17 years old at registration:\n"
        "MELD = [4.56 x ln(bilirubin)] + [0.82 x (137 - sodium)] - "
        "[0.24 x (137 - sodium) x ln(bilirubin)] + [9.09 x ln(INR)] + [11.14 x ln(creatinine)] + "
        "[1.85 x (3.5 - albumin)] - [1.83 x (3.5 - albumin) x ln(creatinine)] + 7.33.\n"
        "Bilirubin, INR, and creatinine values less than 1.0 are set to 1.0. Creatinine is capped at 3.0 mg/dL "
        "and set to 3.0 mg/dL for candidates who had at least two dialysis treatments in the last 7 days or "
        "24 hours of continuous veno-venous hemodialysis (CVVHD). Sodium is capped to 125-137 mmol/L, and "
        "albumin is capped to 1.5-3.5 g/dL. The score is rounded to the nearest whole number and bounded to 6-40.\n"
    )


    creatinine_exp, creatinine = unit_converter_new.conversion_explanation(input_variables["creatinine"][0], "creatinine", 113.12, None, input_variables["creatinine"][1], "mg/dL")
    
    explanation += creatinine_exp + "\n"

    if "dialysis_twice" not in input_variables:
        explanation += "Whether the patient has gone through dialysis at least twice in the past week is not mentioned, and so we assume this to be false.\n"
        input_variables["dialysis_twice"] = False
    elif input_variables["dialysis_twice"]:
        explanation += "The patient is reported to have gone through dialysis at least twice in the past week.\n"
    else:
        explanation += "The patient has not went through dialysis at least twice in the past week.\n"

    if "cvvhd" not in input_variables:
        explanation += "Whether the patient has gone through continuous veno-venous hemodialysis in the past 24 hours is not mentioned, and so we assume this to be false.\n"
        input_variables["cvvhd"] = False
    elif input_variables["cvvhd"]:
        explanation += "The patient is reported to have gone through continuous veno-venous hemodialysis in the past 24 hours.\n"
    else:
        explanation += "The patient is reported to not have done dialysis at least twice in the past week.\n"


    if input_variables["dialysis_twice"] or input_variables["cvvhd"]:
        explanation += "Because the patient has gone through at least one of (i) dialysis two or more times in the past 7 days or (ii) continuous veno-venous hemodialysis in the past 24 hours, we set the creatinine concentration to 3.0 mg/dL.\n"
        creatinine = 3.0
    elif creatinine < 1.0:
        explanation += "The patient's creatinine concentration is less than 1.0 mg/dL, and so we set the creatinine concentration to 1.0 mg/dL.\n"
        creatinine = 1.0
    elif creatinine > 3.0:
        explanation += "The creatinine concentration is greater than 3.0 mg/dL, and so we set the creatinine concentration to 3.0 mg/dL.\n"
        creatinine = 3.0

    bilirubin_exp, bilirubin = unit_converter_new.conversion_explanation(input_variables["bilirubin"][0], "bilirubin", 584.66, None, input_variables["bilirubin"][1], "mg/dL")
    
    explanation += bilirubin_exp 

    if bilirubin < 1.0:
        explanation += "The patient's bilirubin concentration is less than 1.0 mg/dL, and so we set the bilirubin concentration to 1.0 mg/dL.\n"
        bilirubin = 1.0
    else:
        explanation += "\n"
    
    inr = input_variables["inr"]

    explanation += f"The patient's INR is {inr}. "

    if inr < 1.0:
        explanation += "The patient's INR is less than 1.0, and so we set the INR to 1.0.\n"
        inr = 1.0
    else:
        explanation += "\n"

    sodium_exp, sodium = unit_converter_new.conversion_explanation(input_variables["sodium"][0], "sodium", 22.99, 1, input_variables["sodium"][1], "mEq/L")

    explanation += sodium_exp

    if sodium < 125:
        explanation += "The sodium concentration is less than 125 mEq/L, and so we set the sodium concentration to 125 mEq/L.\n"
        sodium = 125
    elif sodium > 137:
        explanation += "The sodium concentration is greater than 137 mEq/L, and so we set the sodium concentration to 137 mEq/L.\n"
        sodium = 137
    else:
        explanation += "\n"

    albumin_exp, albumin = unit_converter_new.conversion_explanation(input_variables["albumin"][0], "albumin", None, None, input_variables["albumin"][1], "g/dL")
    explanation += albumin_exp

    if albumin < 1.5:
        explanation += "The albumin concentration is less than 1.5 g/dL, and so we set the albumin concentration to 1.5 g/dL.\n"
        albumin = 1.5
    elif albumin > 3.5:
        explanation += "The albumin concentration is greater than 3.5 g/dL, and so we set the albumin concentration to 3.5 g/dL.\n"
        albumin = 3.5
    else:
        explanation += "\n"

    if "age" in input_variables:
        age_explanation, age = age_conversion.age_conversion_explanation(input_variables["age"])
        explanation += f"{age_explanation}\n"
    else:
        explanation += "The patient's age is not mentioned, and so we assume the candidate is an adult (at least 18 years old) for MELD 3.0.\n"
        age = 18

    is_adult = age >= 18

    if age < 12:
        explanation += "MELD 3.0 is intended for candidates age 12 or older. A candidate under 12 should receive a PELD score; we proceed with the adolescent MELD 3.0 formula for reference.\n"

    female = 0
    if is_adult:
        if "sex" not in input_variables:
            explanation += "The patient's sex is not mentioned, and so we assume male (no female adjustment).\n"
        else:
            sex = input_variables["sex"]
            explanation += f"The patient's sex is {sex.lower()}, "
            if sex == "Female":
                female = 1
                explanation += "so we add the female adjustment of 1.33.\n"
            else:
                explanation += "so no female adjustment is added.\n"
    else:
        explanation += "Because the candidate was under 18 at registration, the MELD 3.0 adolescent formula does not include a female adjustment.\n"

    # Use capped lab values for the shared base formula before the age split.
    ln_bilirubin = math.log(bilirubin)
    ln_inr = math.log(inr)
    ln_creatinine = math.log(creatinine)
    sodium_term = 137 - sodium
    albumin_term = 3.5 - albumin

    base_meld = (
        4.56 * ln_bilirubin
        + 0.82 * sodium_term
        - 0.24 * sodium_term * ln_bilirubin
        + 9.09 * ln_inr
        + 11.14 * ln_creatinine
        + 1.85 * albumin_term
        - 1.83 * albumin_term * ln_creatinine
    )

    if is_adult:
        meld_raw = 1.33 * female + base_meld + 6
        explanation += (
            "Applying the adult MELD 3.0 formula gives us "
            f"1.33 x {female} + [4.56 x ln({bilirubin})] + [0.82 x (137 - {sodium})] - "
            f"[0.24 x (137 - {sodium}) x ln({bilirubin})] + [9.09 x ln({inr})] + [11.14 x ln({creatinine})] + "
            f"[1.85 x (3.5 - {albumin})] - [1.83 x (3.5 - {albumin}) x ln({creatinine})] + 6 = {meld_raw}.\n"
        )
    else:
        meld_raw = base_meld + 7.33
        explanation += (
            "Applying the adolescent MELD 3.0 formula gives us "
            f"[4.56 x ln({bilirubin})] + [0.82 x (137 - {sodium})] - "
            f"[0.24 x (137 - {sodium}) x ln({bilirubin})] + [9.09 x ln({inr})] + [11.14 x ln({creatinine})] + "
            f"[1.85 x (3.5 - {albumin})] - [1.83 x (3.5 - {albumin}) x ln({creatinine})] + 7.33 = {meld_raw}.\n"
        )

    meldna = round_half_up(meld_raw)
    explanation += f"Rounding to the nearest whole number gives {meldna}.\n"

    if meldna < 6:
        meldna = 6
        explanation += "The minimum MELD score is 6, so we set the score to 6.\n"
    elif meldna > 40:
        meldna = 40
        explanation += "The maximum MELD score is 40, so we set the score to 40.\n"
    else:
        explanation += f"The MELD 3.0 score remains {meldna}.\n"

    return {"Explanation": explanation, "Answer": meldna}
