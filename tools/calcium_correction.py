import unit_converter_new
from rounding import round_number

def calculate_corrected_calcium(albumin=None, calcium=None):
    normal_albumin = 4.0
    albumin = albumin
    albumin_val = albumin[0]
    albumin_units = albumin[1]
    calcium = calcium
    calcium_val = calcium[0]
    calcium_units = calcium[1]
    albumin = unit_converter_new.conversion(albumin_val, 'albmumin', 66500, None, albumin_units, 'g/dL')
    calcium = unit_converter_new.conversion(calcium_val, 'calcium', 40.08, 2, calcium_units, 'mg/dL')
    corrected_calcium = 0.8 * (normal_albumin - albumin) + calcium
    return corrected_calcium
