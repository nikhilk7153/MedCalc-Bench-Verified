import unit_converter_new
from rounding import round_number

def compute_steroid_conversion(input_steroid, target_steroid):
    conversion_dict = {'Betamethasone IV': 1, 'Cortisone PO': 33.33, 'Dexamethasone IV': 1, 'Dexamethasone PO': 1, 'Hydrocortisone IV': 26.67, 'Hydrocortisone PO': 26.67, 'MethylPrednisoLONE IV': 5.33, 'MethylPrednisoLONE PO': 5.33, 'PrednisoLONE PO': 6.67, 'PredniSONE PO': 6.67, 'Triamcinolone IV': 5.33}
    input_drug_mass = unit_converter_new.conversion(input_steroid[1], input_steroid[0], None, None, input_steroid[2], 'mg')
    target_drug_name = target_steroid
    input_drug_name = input_steroid[0]
    input_unit = input_steroid[2]
    from_multiplier = conversion_dict[input_drug_name]
    to_multiplier = conversion_dict[target_drug_name]
    from_multiplier = conversion_dict[input_drug_name]
    to_multiplier = conversion_dict[target_drug_name]
    conversion_factor = to_multiplier / from_multiplier
    converted_amount = input_drug_mass * conversion_factor
    input_drug_mass = input_drug_mass
    return converted_amount
