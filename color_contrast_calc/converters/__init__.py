import math

def rgb_clamp(vals):
    return tuple(_adjusted_round(max(0, min(255, c))) for c in vals)

def _adjusted_round(n):
    if math.modf(n)[0] == 0.5:
        return math.ceil(n)
    else:
        return round(n)

