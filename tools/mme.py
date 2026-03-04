import unit_converter_new
from rounding import round_number

def mme(codeine_dose=None, codeine_dose_per_day=None, fentanyl_buccal_dose=None, fentanyl_buccal_dose_per_day=None, fentanyl_patch_dose=None, fentanyl_patch_dose_per_day=None, hydrocodone_dose=None, hydrocodone_dose_per_day=None, hydromorphone_dose=None, hydromorphone_dose_per_day=None, methadone_dose=None, methadone_dose_per_day=None, morphine_dose=None, morphine_dose_per_day=None, oxycodone_dose=None, oxycodone_dose_per_day=None, oxymorphone_dose=None, oxymorphone_dose_per_day=None, tapentadol_dose=None, tapentadol_dose_per_day=None, tramadol_dose=None, tramadol_dose_per_day=None, buprenorphine_dose=None, buprenorphine_dose_per_day=None):

    def _per_day(value):
        if value is None:
            return None
        if isinstance(value, (list, tuple)):
            return value[0]
        return value

    def _component(dose, per_day, drug_name, target_unit, factor):
        if dose is None or per_day is None:
            return 0
        amount = unit_converter_new.conversion(dose[0], drug_name, None, None, dose[1], target_unit)
        return amount * _per_day(per_day) * factor
    mme_equivalent = 0
    mme_equivalent += _component(codeine_dose, codeine_dose_per_day, 'Codeine', 'mg', 0.15)
    mme_equivalent += _component(fentanyl_buccal_dose, fentanyl_buccal_dose_per_day, 'FentaNYL buccal', 'µg', 0.13)
    mme_equivalent += _component(fentanyl_patch_dose, fentanyl_patch_dose_per_day, 'FentANYL patch', 'µg', 2.4)
    mme_equivalent += _component(hydrocodone_dose, hydrocodone_dose_per_day, 'HYDROcodone', 'mg', 1)
    mme_equivalent += _component(hydromorphone_dose, hydromorphone_dose_per_day, 'HYDROmorphone', 'mg', 5)
    mme_equivalent += _component(methadone_dose, methadone_dose_per_day, 'Methadone', 'mg', 4.7)
    mme_equivalent += _component(morphine_dose, morphine_dose_per_day, 'Morphine', 'mg', 1)
    mme_equivalent += _component(oxycodone_dose, oxycodone_dose_per_day, 'OxyCODONE', 'mg', 1.5)
    mme_equivalent += _component(oxymorphone_dose, oxymorphone_dose_per_day, 'OxyMORphone', 'mg', 3)
    mme_equivalent += _component(tapentadol_dose, tapentadol_dose_per_day, 'Tapentadol', 'mg', 0.4)
    mme_equivalent += _component(tramadol_dose, tramadol_dose_per_day, 'TraMADol', 'mg', 0.2)
    mme_equivalent += _component(buprenorphine_dose, buprenorphine_dose_per_day, 'Buprenorphine', 'mg', 10)
    return mme_equivalent
