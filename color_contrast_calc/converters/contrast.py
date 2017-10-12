# https://www.w3.org/TR/filter-effects/#funcdef-contrast
# https://www.w3.org/TR/SVG/filters.html#TransferFunctionElementAttributes

from . import rgb_clamp


def calc_rgb(rgb, ratio=100):
    r = float(ratio)
    return rgb_clamp((c * r + 255 * (50 - r / 2)) / 100 for c in rgb)
