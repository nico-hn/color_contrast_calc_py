'''Implement a function that corresponds to a CSS filter contrast().

* https://www.w3.org/TR/filter-effects/#funcdef-contrast
* https://www.w3.org/TR/SVG/filters.html#TransferFunctionElementAttributes
'''

# https://www.w3.org/TR/filter-effects/#funcdef-contrast
# https://www.w3.org/TR/SVG/filters.html#TransferFunctionElementAttributes

from . import rgb_clamp


def calc_rgb(rgb, ratio=100):
    """Return contrast adjusted RGB value of passed color.

    The calculation is based on the definition found at
    https://www.w3.org/TR/filter-effects/#funcdef-contrast
    :param rgb: The Original RGB value before the adjustment.
    :type rgb: (int, int, int)
    :param ratio: Adjustment ratio in percentage [optional]
    :type ratio: float
    :return: Contrast adjusted RGB value
    :rtype: (int, int, int)
    """
    r = float(ratio)
    return rgb_clamp((c * r + 255 * (50 - r / 2)) / 100 for c in rgb)
