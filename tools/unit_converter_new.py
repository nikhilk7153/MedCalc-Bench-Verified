from rounding import round_number

def vol_to_vol(value, src_unit, tgt_unit, conversion_factor=False):
    conversion_factors_l = {'L': 1, 'dL': 0.1, 'mL': 0.001, 'µL': 1e-06, 'mm^3': 1e-06, 'cm^3': 0.001, 'm^3': 1000}
    if src_unit == tgt_unit:
        return value
    if conversion_factor:
        return conversion_factors_l[src_unit] / conversion_factors_l[tgt_unit]
    factor = conversion_factors_l[src_unit] / conversion_factors_l[tgt_unit]
    return value * factor

def molg_to_molg(mass, src_unit, tgt_unit):
    conversion_factors_mol = {'mol': 1, 'mmol': 0.001, 'µmol': 1e-06, 'pmol': 1e-09}
    conversion_factors_g = {'kg': 1000, 'g': 1, 'mg': 0.001, 'µg': 1e-06}
    if src_unit == tgt_unit:
        return mass
    if 'mol' in src_unit and 'mol' in tgt_unit:
        factors = conversion_factors_mol
    else:
        factors = conversion_factors_g
    return mass * (factors[src_unit] / factors[tgt_unit])

def mol_g(value, molar_mass, src_unit, tgt_unit):
    mol = molg_to_molg(value, src_unit, 'mol')
    grams = mol * molar_mass
    return molg_to_molg(grams, 'g', tgt_unit)

def g_to_mol(value, molar_mass, src_unit, tgt_unit):
    grams = molg_to_molg(value, src_unit, 'g')
    mol = grams / molar_mass
    return molg_to_molg(mol, 'mol', tgt_unit)

def mEq_to_mol(value, valence, tgt_unit):
    mol = value / valence
    if tgt_unit != 'mmol':
        return molg_to_molg(mol, 'mmol', tgt_unit)
    return mol

def mol_to_mEq(value, valence, src_unit):
    mmol_value = value
    if src_unit != 'mmol':
        mmol_value = molg_to_molg(value, src_unit, 'mmol')
    return mmol_value * valence

def mEq_to_g(value, molar_mass, valence, tgt_unit):
    mmol_val = value / valence
    mol_value = molg_to_molg(mmol_val, 'mmol', 'mol')
    return mol_g(mol_value, molar_mass, 'mol', tgt_unit)

def g_to_mEq(value, molar_mass, valence, src_unit):
    mol_value = g_to_mol(value, molar_mass, src_unit, 'mmol')
    return mol_value * valence

def mass_conversion(value, valence, molar_mass, src_mass_unit, tgt_mass_unit):
    if 'g' in src_mass_unit and 'g' in tgt_mass_unit or ('mol' in src_mass_unit and 'mol' in tgt_mass_unit):
        return molg_to_molg(value, src_mass_unit, tgt_mass_unit)
    if 'mol' in src_mass_unit and 'g' in tgt_mass_unit:
        return mol_g(value, molar_mass, src_mass_unit, tgt_mass_unit)
    if 'g' in src_mass_unit and 'mol' in tgt_mass_unit:
        return g_to_mol(value, molar_mass, src_mass_unit, tgt_mass_unit)
    if 'mol' in src_mass_unit and 'mEq' in tgt_mass_unit:
        return mol_to_mEq(value, valence, src_mass_unit)
    if 'mEq' in src_mass_unit and 'mol' in tgt_mass_unit:
        return mEq_to_mol(value, valence, tgt_mass_unit)
    if 'mEq' in src_mass_unit and 'g' in tgt_mass_unit:
        return mEq_to_g(value, molar_mass, valence, tgt_mass_unit)
    if 'g' in src_mass_unit and 'mEq' in tgt_mass_unit:
        return g_to_mEq(value, molar_mass, valence, src_mass_unit)
    return value

def conversion(value, compound, molar_mass, valence, src_unit, tgt_unit):
    del compound
    conversion_factors_mass = {'mol', 'mmol', 'µmol', 'pmol', 'kg', 'g', 'mg', 'µg', 'mEq'}
    conversion_factors_volume = {'L', 'dL', 'mL', 'µL', 'mm^3', 'cm^3', 'm^3'}
    if '/' in src_unit and '/' in tgt_unit:
        src_mass_unit, src_volume_unit = src_unit.split('/')
        tgt_mass_unit, tgt_volume_unit = tgt_unit.split('/')
        if src_mass_unit == tgt_mass_unit and src_volume_unit == tgt_volume_unit:
            return value
        if src_mass_unit != tgt_mass_unit:
            mass_value = mass_conversion(value, valence, molar_mass, src_mass_unit, tgt_mass_unit)
        else:
            mass_value = value
        if src_volume_unit == tgt_volume_unit:
            return mass_value
        volume_conversion_factor = vol_to_vol(1, src_volume_unit, tgt_volume_unit, True)
        return mass_value / volume_conversion_factor
    if ('/' not in src_unit and '/' not in tgt_unit) and src_unit in conversion_factors_mass and (tgt_unit in conversion_factors_mass):
        if src_unit == tgt_unit:
            return value
        return mass_conversion(value, valence, molar_mass, src_unit, tgt_unit)
    if ('/' not in src_unit and '/' not in tgt_unit) and src_unit in conversion_factors_volume and (tgt_unit in conversion_factors_volume):
        if src_unit == tgt_unit:
            return value
        return vol_to_vol(value, src_unit, tgt_unit)
    return value

def convert_to_units_per_liter(value, unit, compound, target_unit):
    del compound
    unit_to_liter = {'L': 1, 'dL': 0.1, 'mL': 0.001, 'µL': 1e-06, 'mm^3': 1e-06, 'cm^3': 0.001, 'm^3': 1000.0}
    if unit == target_unit:
        return value
    conversion_factor = unit_to_liter[target_unit] / unit_to_liter[unit]
    return conversion_factor * value

def mmHg_to_kPa(mmHg, compound):
    del compound
    return 0.133322 * mmHg

def kPa_to_mmHg(kPa, compound):
    del compound
    return 7.50062 * kPa
