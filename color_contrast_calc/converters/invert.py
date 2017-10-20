# https://www.w3.org/TR/filter-effects/#funcdef-invert
# https://www.w3.org/TR/filter-effects-1/#invertEquivalent
# https://www.w3.org/TR/SVG/filters.html#TransferFunctionElementAttributes


def calc_rgb(rgb, ratio):
    """Return an inverted RGB value of passed color.

    The calculation is based on the definition found at
    https://www.w3.org/TR/filter-effects/#funcdef-invert
    :param rgb: The Original RGB value before the inversion.
    :type rgb: (int, int, int)
    :param ratio: Proportion of the conversion in percentage.
    :type ratio: float
    :return: Inverted RGB value
    :rtype: (int, int, int)
    """
    r = float(ratio)
    return tuple(round((100 * c - 2 * c * r + 255 * r) / 100) for c in rgb)
