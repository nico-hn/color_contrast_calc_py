import math


def rgb_clamp(vals):
    """Clamp the value of each RGB component to the range of 0 to 255"""
    return tuple(_adjusted_round(max(0, min(255, c))) for c in vals)


def _adjusted_round(n):
    if math.modf(n)[0] == 0.5:
        return int(math.ceil(n))

    return int(round(n))
