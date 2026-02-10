import unit_converter_new
from rounding import round_number

def mme_explanation(input_parameters):

    explanation = """The Opioid Conversion Table with MME (Morphine Milligram Equivalent) conversion factors based on the CDC Clinical Practice Guideline for Prescribing Opioids for Pain — United States, 2022 are listed below:

1. Codeine: MME conversion factor = 0.15
2. FentaNYL patch: MME conversion factor = 2.4
3. HYDROcodone: MME conversion factor = 1
4. HYDROmorphone: MME conversion factor = 5
5. Methadone: MME conversion factor = 4.7
6. Morphine: MME conversion factor = 1
7. OxyCODONE: MME conversion factor = 1.5
8. OxyMORphone: MME conversion factor = 3
9. Tapentadol: MME conversion factor = 0.4
10. TraMADol: MME conversion factor = 0.2
"""
    
    mme_drug = {"Codeine": 0.15, 
            "FentaNYL patch": 2.4,
            "HYDROcodone": 1,
            "HYDROmorphone": 5,
            "Methadone": 4.7, 
            "Morphine": 1, 
            "OxyCODONE": 1.5, 
            "OxyMORphone": 3, 
            "Tapentadol": 0.4, 
            "TraMADol": 0.2}

    name_aliases = {
        "FentANYL patch": "FentaNYL patch",
        "Fentanyl patch": "FentaNYL patch",
        "Fentanyl Patch": "FentaNYL patch",
    }

    explanation += "\nThe curent Morphine Milligram Equivalents (MME) is 0 MME per day.\n"
    
    mme_equivalent = 0
    
    for drug_name in input_parameters:
        if "Day" in drug_name:
            continue 

        raw_name = drug_name.split(" Dose")[0]
        name = name_aliases.get(raw_name, raw_name)

        units = input_parameters[raw_name + " Dose"][1]

        if name not in mme_drug:
            raise ValueError(f"Unsupported opioid for MME conversion: {name}")

        if name != "FentaNYL patch":
            drug_mg_exp, drug_mg = unit_converter_new.conversion_explanation(
                input_parameters[raw_name + " Dose"][0], name, None, None, units, "mg"
            )
            if units == "mg":
                explanation += f"The patient's dose of {name} is {drug_mg} mg. "
            else:
                explanation += f"The patient's dose of {name} is measured in {units}. We need to convert this to mg. "
                explanation += drug_mg_exp + "\n"
        else:
            raw_value = input_parameters[raw_name + " Dose"][0]
            if units in ["µg/hr", "mcg/hr"]:
                drug_mg = raw_value
                explanation += f"The patient's dose of {name} is {drug_mg} µg/hr.\n"
            elif units in ["µg", "mcg"]:
                drug_mg = raw_value
                explanation += f"The patient's dose of {name} is provided as {drug_mg} µg and interpreted as µg/hr.\n"
            else:
                drug_mg_exp, drug_mg = unit_converter_new.conversion_explanation(
                    raw_value, name, None, None, units, "µg/hr"
                )
                explanation += f"The patient's dose of {name} is measured in {units}. We need to convert this to µg/hr. "
                explanation += drug_mg_exp + "\n"


        if name == "FentaNYL patch":
            total_per_day = drug_mg
            rounded_total_per_day = round_number(total_per_day)
            explanation += f"The patient's fentanyl patch dose is interpreted as {rounded_total_per_day} µg/hr. "
            mme_increase = mme_drug[name] * total_per_day
            explanation += f"To convert to mme/day of {name}, multiply the {rounded_total_per_day} µg/hr by the mme conversion factor, {mme_drug[name]} mme/(µg/hr), giving us {round_number(mme_increase)} mme/day. "
        else:
            target_unit = "mg"
            dose_per_day_key = raw_name + " Dose Per Day"
            dose_per_day = input_parameters[dose_per_day_key][0]
            total_per_day = drug_mg * dose_per_day
            rounded_total_per_day = round_number(total_per_day)
            explanation += f"The patient takes {dose_per_day} doses/day of {name}. This means that the patient takes {round_number(drug_mg)} {target_unit}/dose {name} * {dose_per_day} dose/day = {rounded_total_per_day} {target_unit}/day. "
            mme_increase = mme_drug[name] * total_per_day
            explanation += f"To convert to mme/day of {name}, multiply the {rounded_total_per_day} {target_unit}/day by the mme conversion factor, {mme_drug[name]} mme/{target_unit}, giving us {round_number(mme_increase)} mme/day. "
    
        explanation += f"Adding the mme/day of {name} to the total mme/day gives us {round_number(mme_equivalent)} + {round_number(mme_increase)} = {round_number(mme_equivalent + mme_increase)} mme/day.\n"

        mme_equivalent += mme_increase


    mme_equivalent = round_number(mme_equivalent)
    explanation += f"The patient's mme/day is {mme_equivalent} mme/day."
        
    return {"Explanation": explanation, "Answer": mme_equivalent}
