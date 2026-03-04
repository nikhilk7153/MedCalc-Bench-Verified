import age_conversion

def compute_perc_rule(age, heart_rate, oxygen_sat, previous_dvt=None, previous_pe=None, unilateral_leg_swelling=False, hemoptysis=False, recent_surgery_or_trauma=False, hormonal_use=False):
    perc_count = 0
    age = age_conversion.age_conversion(age)
    heart_rate = heart_rate[0]
    oxygen_sat = oxygen_sat[0]
    if age >= 50:
        perc_count += 1
    if heart_rate >= 100:
        perc_count += 1
    if oxygen_sat < 95:
        perc_count += 1
    if previous_dvt is True or previous_pe is True:
        perc_count += 1
    if unilateral_leg_swelling:
        perc_count += 1
    if hemoptysis:
        perc_count += 1
    if recent_surgery_or_trauma:
        perc_count += 1
    if hormonal_use:
        perc_count += 1
    return perc_count
