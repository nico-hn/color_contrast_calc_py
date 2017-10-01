# https://www.w3.org/TR/filter-effects-1/#invertEquivalent
# https://www.w3.org/TR/SVG/filters.html#TransferFunctionElementAttributes

def calc_rgb(rgb, ratio):
    r = float(ratio)
    return tuple(round((100 * c - 2 * c * r + 255 * r) / 100) for c in rgb)
