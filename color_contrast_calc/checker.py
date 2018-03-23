'''Utility to check properties of given colors.

This module provides functions that check the relative luminance and
contrast ratio of colors.  A color is given as RGB value (represented
as a tuple of integers) or a hex color code such "#ffff00".
'''

from . import utils
from . import const

class WCAGLevel:
    '''Class used as name space for contrast ratio related constants.'''
    A = 'A'
    AA = 'AA'
    AAA = 'AAA'

_LEVEL_TO_RATIO = {
    WCAGLevel.AAA: 7,
    WCAGLevel.AA: 4.5,
    WCAGLevel.A: 3,
}


# https://www.w3.org/TR/2008/REC-WCAG20-20081211/#relativeluminancedef

def relative_luminance(rgb):
    """Calculate the relative luminance of a RGB color.

    The definition of relative luminance is given at
    https://www.w3.org/TR/2008/REC-WCAG20-20081211/#relativeluminancedef
    :param rgb: RGB color given as a string or a tuple of integers.
                Yellow, for example, can be given as "#ffff00" or
                (255, 255, 0).
    :type rgb: str or (int, int, int)
    :return: Relative luminance of the passed color.
    :rtype: float
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

    return pow((s + 0.055) / 1.055, 2.4)


# https://www.w3.org/TR/2008/REC-WCAG20-20081211/#contrast-ratiodef

def contrast_ratio(color1, color2):
    """Calculate the contrast ratio of given colors.

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
    :rtype: float
    """
    return luminance_to_contrast_ratio(relative_luminance(color1),
                                       relative_luminance(color2))


def luminance_to_contrast_ratio(luminance1, luminance2):
    """Calculate contrast ratio from a pair of relative luminance.

    :param luminance1: Relative luminance
    :type luminance1: float
    :param luminance2: Relative luminance
    :type luminance2: float
    :return: Contrast ratio
    :rtype: float
    """
    (l1, l2) = sorted((luminance1, luminance2), reverse=True)
    return (l1 + 0.05) / (l2 + 0.05)


def ratio_to_level(ratio):
    """Rate a given contrast ratio according to the WCAG 2.0 criteria.

    The success criteria are given at
    https://www.w3.org/TR/WCAG20/#visual-audio-contrast
    https://www.w3.org/TR/WCAG20-TECHS/G183.html

    N.B. The size of text is not taken into consideration.
    :param ratio: Contrast ratio
    :type ratio: float
    :return: If one of criteria is satisfied, "A", "AA" or "AAA",
             otherwise "-"
    :rtype: str
    """
    if ratio >= 7:
        return WCAGLevel.AAA
    if ratio >= 4.5:
        return WCAGLevel.AA
    if ratio >= 3:
        return WCAGLevel.A

    return '-'


def level_to_ratio(level):
    """Return a contrast ratio required to meet a given WCAG 2.0 level.

    N.B. The size of text is not taken into consideration.
    :param level: "A", "AA" or "AAA"
    :type level: str
    :return: Contrast ratio
    :rtype: float
    """
    if isinstance(level, (int, float)) and level >= 1.0 and level <= 21.0:
        return level

    if level in _LEVEL_TO_RATIO:
        return _LEVEL_TO_RATIO[level]

    return None


def is_light_color(rgb):
    """Check if the contrast ratio against black is higher than
       against white.

    :param rgb: RGB color given as a string or a tuple of integers.
    :type rgb: str or (int, int, int)
    :return: True if the contrast ratio against white is qual to or
             less than the ratio against black
    :rtype: bool
    """
    lum = relative_luminance(rgb)
    ratio_with_white = luminance_to_contrast_ratio(const.luminance.WHITE, lum)
    ratio_with_black = luminance_to_contrast_ratio(const.luminance.BLACK, lum)
    return ratio_with_white <= ratio_with_black
