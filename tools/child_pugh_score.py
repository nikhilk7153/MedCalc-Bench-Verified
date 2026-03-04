import unit_converter_new

def compute_child_pugh_score(inr, ascites, bilirubin, albumin, encephalopathy=None):
    cp_score = 0
    inr = float(inr)
    ascites_state = ascites if ascites is not None else 'absent'
    encephalopathy_state = encephalopathy if encephalopathy is not None else 'No Encephalopathy'
    bilirubin = unit_converter_new.conversion(bilirubin[0], 'bilirubin', 584.66, None, bilirubin[1], 'mg/dL')
    albumin = unit_converter_new.conversion(albumin[0], 'albumin', 66500, None, albumin[1], 'g/dL')
    if inr < 1.7:
        cp_score += 1
    elif 1.7 <= inr <= 2.3:
        cp_score += 2
    elif inr > 2.3:
        cp_score += 3
    if bilirubin < 2:
        cp_score += 1
    elif 2 <= bilirubin <= 3:
        cp_score += 2
    elif bilirubin > 3:
        cp_score += 3
    if albumin > 3.5:
        cp_score += 1
    elif 2.8 <= albumin <= 3.5:
        cp_score += 2
    elif albumin < 2.8:
        cp_score += 3
    if ascites is not None:
        if ascites == 'absent':
            cp_score += 1
        elif ascites_state == 'slight':
            cp_score += 2
        elif ascites_state == 'moderate':
            cp_score += 3
    else:
        cp_score += 1
    if encephalopathy is not None:
        if encephalopathy_state == 'No Encephalopathy':
            cp_score += 1
        elif encephalopathy_state == 'Grade 1-2':
            cp_score += 2
        elif encephalopathy_state == 'Grade 3-4':
            cp_score += 3
    else:
        cp_score += 1
    return cp_score
