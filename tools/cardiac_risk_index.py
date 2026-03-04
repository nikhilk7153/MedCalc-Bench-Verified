import json
import unit_converter_new

def compute_cardiac_index(pre_operative_creatinine, elevated_risk_surgery=False, ischemic_heart_disease=False, congestive_heart_failure=False, cerebrovascular_disease=False, pre_operative_insulin_treatment=False):
    cri = 0
    cri += 1 if elevated_risk_surgery else 0
    cri += 1 if ischemic_heart_disease else 0
    cri += 1 if congestive_heart_failure else 0
    cri += 1 if cerebrovascular_disease else 0
    cri += 1 if pre_operative_insulin_treatment else 0
    creatinine_val = unit_converter_new.conversion(pre_operative_creatinine[0], 'Pre-Operative Creatinine', 113.12, None, pre_operative_creatinine[1], 'mg/dL')
    if creatinine_val > 2:
        cri += 1
    return cri
