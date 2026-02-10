import unit_converter_new
from rounding import round_number


def compute_serum_osmolality_explanation(input_parameters):

    explanation = "The formula for computing serum osmolality is 2 * Na + (BUN / 2.8) + (glucose / 18), where Na is the concentration of sodium in mmol/L, the concentration of BUN is in mg/dL, and the concentration of glucose is in mg/dL.\n"
    explanation += "If BUN is provided in mmol/L, it is treated as urea mmol/L (same numeric value) and converted to mg/dL using the 2.8 factor.\n"
    explanation += "If BUN is provided in mmol/L, it is treated as urea mmol/L (same numeric value) and converted to mg/dL by multiplying by 2.8.\n"
    
    # Na is scored in mmol/L; BUN and glucose are scored in mg/dL in this formula.
    sodium_exp, sodium = unit_converter_new.conversion_explanation(input_parameters["sodium"][0], "sodium", 22.99, 1, input_parameters["sodium"][1], "mmol/L")
    bun_exp, bun = unit_converter_new.conversion_explanation(input_parameters["bun"][0], "bun", 28.02, None, input_parameters["bun"][1], "mg/dL")
    glucose_exp, glucose = unit_converter_new.conversion_explanation(input_parameters["glucose"][0], "glucose", 180.16, None, input_parameters["glucose"][1], "mg/dL")

    explanation += sodium_exp + "\n"
    explanation += bun_exp + "\n"
    explanation += glucose_exp + "\n"

    # Formula uses Na in mmol/L, BUN in mg/dL, glucose in mg/dL.
    serum_os = round_number(2 * sodium + (bun / 2.8) + (glucose / 18))

    explanation += f"Plugging these values into the equation, we get 2 * {sodium} + ({bun} / 2.8) + ({glucose} / 18) = {serum_os} mOsm/kg."
    explanation += f"The patient's calculated serum osmolality concentration is {serum_os} mOsm/kg."

    return {"Explanation": explanation, "Answer": serum_os}
