# https://www.w3.org/TR/filter-effects/#funcdef-brightness
# https://www.w3.org/TR/SVG/filters.html#TransferFunctionElementAttributes

from . import rgb_clamp


def calc_rgb(rgb, ratio=100):
    """Return brightness adjusted RGB value of passed color.

    The calculation is based on the definition found at
    https://www.w3.org/TR/filter-effects/#funcdef-brightness
    :param rgb: The Original RGB value before the adjustment.
    :type rgb: (int, int, int)
    :param ratio: Adjustment ratio in percentage [optional]
    :type ratio: float
    :return: Brightness adjusted RGB value
    :rtype: (int, int, int)
    """
    r = float(ratio)
    return rgb_clamp(c * r / 100 for c in rgb)
