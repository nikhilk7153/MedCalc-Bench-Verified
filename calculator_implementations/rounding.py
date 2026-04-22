from math import log10, floor

def round_number(num):
    """
    Rounds to at least 5 decimal places, but extends further if needed so that
    5 significant digits are preserved (e.g. 0.000134 stays 0.000134, not 0.00013).
    """
    if num == 0:
        return 0

    sig_digits_needed = -int(floor(log10(abs(num)))) + 4
    return round(num, max(5, sig_digits_needed))
