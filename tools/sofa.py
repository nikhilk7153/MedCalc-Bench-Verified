import unit_converter_new
from rounding import round_number

def compute_sofa(pao2, fio2, mechanical_ventilation, cpap, gcs, bilirubin, platelet_count, creatinine, urine_output, sys_bp=None, dia_bp=None, dopamine=None, dobutamine=None, epinephrine=None, norepinephrine=None, mechanical_ventillation=None):
    sofa_score = 0
    pao2 = pao2[0]
    fio2 = fio2[0]
    dopamine = dopamine if dopamine is not None else [0]
    dobutamine = dobutamine if dobutamine is not None else [0]
    epinephrine = epinephrine if epinephrine is not None else [0]
    norepinephrine = norepinephrine if norepinephrine is not None else [0]
    ratio = pao2 / (fio2 / 100)
    if mechanical_ventilation is None:
        mechanical_ventilation = False
    elif mechanical_ventilation:
        pass
    else:
        mechanical_ventilation = False
    if cpap is None:
        cpap = False
    if ratio >= 400:
        pass
    elif 300 <= ratio < 400:
        sofa_score += 1
    elif 200 <= ratio < 300:
        sofa_score += 2
    elif ratio <= 199 and (mechanical_ventillation is None and cpap is None or (not mechanical_ventilation and (not cpap))):
        sofa_score += 2
    elif 100 <= ratio < 199 and (mechanical_ventilation or cpap):
        sofa_score += 3
    elif ratio < 100 and (mechanical_ventilation or cpap):
        sofa_score += 4
    if dopamine[0] > 15 or epinephrine[0] > 0.1 or norepinephrine[0] > 0.1:
        sofa_score += 4
    elif dopamine[0] > 5 or 0 < epinephrine[0] <= 0.1 or 0 < norepinephrine[0] <= 0.1:
        sofa_score += 3
    elif 0 < dopamine[0] <= 5 or dobutamine[0]:
        sofa_score += 2
    elif (sys_bp is not None and dia_bp is not None) and 1 / 3 * sys_bp[0] + 2 / 3 * dia_bp[0] < 70 and (not dobutamine[0] and (not epinephrine[0]) and (not norepinephrine[0])):
        sys_bp = sys_bp[0]
        dia_bp = dia_bp[0]
        map = 1 / 3 * sys_bp + 2 / 3 * dia_bp
        sofa_score += 1
    if gcs is not None:
        gcs = gcs[0] if isinstance(gcs, (list, tuple)) else gcs
    else:
        gcs = 15
    if gcs < 6:
        sofa_score += 4
    elif 6 <= gcs <= 9:
        sofa_score += 3
    elif 10 <= gcs <= 12:
        sofa_score += 2
    elif 13 <= gcs <= 14:
        sofa_score += 1
    bilirubin = unit_converter_new.conversion(bilirubin[0], 'bilirubin', 584.66, None, bilirubin[1], 'mg/dL')
    if bilirubin < 1.2:
        pass
    elif 1.2 <= bilirubin < 2.0:
        sofa_score += 1
    elif 2.0 <= bilirubin < 6.0:
        sofa_score += 2
    elif 6.0 <= bilirubin < 12.0:
        sofa_score += 3
    elif bilirubin >= 12.0:
        sofa_score += 4
    platelet_count = unit_converter_new.convert_to_units_per_liter(platelet_count[0], platelet_count[1], 'platelet', 'µL')
    if 100000 <= platelet_count < 150000:
        sofa_score += 1
    elif 50000 <= platelet_count < 100000:
        sofa_score += 2
    elif 20000 <= platelet_count < 50000:
        sofa_score += 3
    elif platelet_count < 20000:
        sofa_score += 4
    creatinine_value = 0
    if creatinine is not None:
        creatinine_value = unit_converter_new.conversion(creatinine[0], 'creatinine', 113.12, None, creatinine[1], 'mg/dL')
    if urine_output is not None:
        urine_output = urine_output[0]
    if creatinine_value > 5.0 or (urine_output is not None and urine_output < 200):
        sofa_score += 4
    elif 3.5 <= creatinine_value <= 5.0 or (urine_output is not None and urine_output < 500):
        sofa_score += 3
    elif 2.0 <= creatinine_value < 3.5:
        sofa_score += 2
    elif 1.2 <= creatinine_value < 2.0:
        sofa_score += 1
    return sofa_score
