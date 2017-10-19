# Utility to check properties of given colors

from . import utils

class WCAGLevel:
    A = 'A'
    AA = 'AA'
    AAA = 'AAA'

_LEVEL_TO_RATIO = {
    WCAGLevel.AAA: 7,
    WCAGLevel.AA: 4.5,
    WCAGLevel.A: 3,
    3: 7,
    2: 4.5,
    1: 3
}


# https://www.w3.org/TR/2008/REC-WCAG20-20081211/#relativeluminancedef

def relative_luminance(rgb):
    """Calculates the relative luminance of a RGB color

    The definition of relative luminance is given at
    https://www.w3.org/TR/2008/REC-WCAG20-20081211/#relativeluminancedef
    :param rgb: RGB color given as a string or a tuple of integers.
                Yellow, for example, can be given as "#ffff00" or
                (255, 255, 0).
    :type rgb: str or (int, int, int)
    :return: Relative luminance of the passed color defined at
    :rtype: number
    """
    if isinstance(rgb, str):
        rgb = utils.hex_to_rgb(rgb)

    (r, g, b) = (_tristimulus_value(c) for c in rgb)
    return r * 0.2126 + g  * 0.7152 + b * 0.0722


def _tristimulus_value(primary_color):
    base = 255
    s = float(primary_color) / base

    if s <= 0.03928:
        return s / 12.92
    else:
        return pow((s + 0.055) / 1.055, 2.4)


# https://www.w3.org/TR/2008/REC-WCAG20-20081211/#contrast-ratiodef

def contrast_ratio(color1, color2):
    """Calculates the contrast ratio of given colors

    The definition of contrast ratio is given at
    https://www.w3.org/TR/2008/REC-WCAG20-20081211/#contrast-ratiodef
    :param color1: RGB color given as a string or a tuple of integers.
                   Yellow, for example, can be given as "#ffff00" or
                   (255, 255, 0).
    :type color1: str or (int, int, int)
    :param color2: RGB color given as a string or a tuple of integers.
                   Yellow, for example, can be given as "#ffff00" or
                   (255, 255, 0).
    :type color2: str or (int, int, int)
    :return: Contrast ratio
    :rtype: number
    """
    return luminance_to_contrast_ratio(relative_luminance(color1),
                                       relative_luminance(color2))


def luminance_to_contrast_ratio(luminance1, luminance2):
    """Calculates contrast ratio from a pair of relative luminance

    :param luminance1: Relative luminance
    :type luminance1: number
    :param luminance2: Relative luminance
    :type luminance2: number
    :return: Contrast ratio
    :rtype: number
    """
    (l1, l2) = sorted((luminance1, luminance2), reverse=True)
    return (l1 + 0.05) / (l2 + 0.05)


def ratio_to_level(ratio):
    if ratio >= 7:
        return WCAGLevel.AAA
    if ratio >= 4.5:
        return WCAGLevel.AA
    if ratio >= 3:
        return WCAGLevel.A

    return '-'


def level_to_ratio(level):
    if level in _LEVEL_TO_RATIO:
        return _LEVEL_TO_RATIO[level]

    return None
