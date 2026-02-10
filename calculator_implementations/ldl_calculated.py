import unit_converter_new
from rounding import round_number

def compute_ldl_explanation(input_parameters):

    explanation = "To compute the patient's LDL cholestrol, apply the following formula: LDL cholesterol = total cholesterol - HDL - (triglycerides / 5), where the units for total cholestrol, HDL cholesterol, and triglycerides are all mg/dL.\n"

    total_cholestrol_exp, total_cholestrol = unit_converter_new.conversion_explanation(input_parameters["total_cholesterol"][0], "total cholesterol", 386.654, None, input_parameters["total_cholesterol"][1], "mg/dL")
    hdl_cholestrol_exp, hdl_cholestrol = unit_converter_new.conversion_explanation(input_parameters["hdl_cholesterol"][0], "hdl cholesterol", 386.654, None, input_parameters["hdl_cholesterol"][1], "mg/dL")
    triglycerides_exp, triglycerides = unit_converter_new.conversion_explanation(input_parameters["triglycerides"][0], "triglycerides", 861.338, None, input_parameters["triglycerides"][1], "mg/dL")

    explanation += total_cholestrol_exp + '\n'
    explanation += hdl_cholestrol_exp + '\n'
    explanation += triglycerides_exp +  '\n'

    if triglycerides >= 400:
        explanation += "Warning: The Friedewald formula is not validated when triglycerides are >= 400 mg/dL; any calculated LDL is unreliable.\n"

    # Friedewald formula uses triglycerides/5 when inputs are in mg/dL.
    answer = round_number(total_cholestrol - hdl_cholestrol - (triglycerides/5))

    explanation += f"Plugging in these values will give us {total_cholestrol} mg/dL - {hdl_cholestrol} mg/dL - ({triglycerides}/5) mg/dL = {answer} mg/dL.\n"

    explanation += f"The patients concentration of LDL cholestrol is {answer} mg/dL."

    return {"Explanation": explanation, "Answer": answer}
