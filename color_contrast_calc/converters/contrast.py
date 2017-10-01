# https://www.w3.org/TR/filter-effects/#funcdef-contrast
# https://www.w3.org/TR/SVG/filters.html#TransferFunctionElementAttributes

import math

def rgb_clamp(vals):
    return tuple(_adjusted_round(max(0, min(255, c))) for c in vals)

def _adjusted_round(n):
    if math.modf(n)[0] == 0.5:
        return math.ceil(n)
    else:
        return round(n)

def calc_rgb(rgb, ratio = 100):
    r = float(ratio)
    return rgb_clamp((c * r + 255 * (50 - r / 2)) / 100 for c in rgb)
