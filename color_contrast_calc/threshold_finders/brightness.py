'''Module that implements the main logic of the instance method
``Color.find_brightness_threshold``.
'''

import math

from .. import const
from .. import checker
from ..converters.brightness import calc_rgb
from . import binary_search_width
from .criteria import threshold_criteria


def find(fixed_color, other_color, level=checker.WCAGLevel.AA):
    """Try to find a color who has a satisfying contrast ratio.

    The color returned by this function will be created by changing the
    brightness of ``other_color``.  Even when a color that satisfies the
    specified level is not found, the function returns a new color
    anyway.
    :param fixed_color: The color which remains unchanged
    :type fixed_color: Color
    :param other_color: Color before the adjustment of brightness
    :type other_color: Color
    :param level: "A", "AA" or "AAA" [optional]
    :type level: str
    :return: New RGB value whose brightness is adjusted from that of
             ``other_color``
    :rtype: (int, int, int)
    """
    color_class = other_color.__class__
    criteria = threshold_criteria(level, fixed_color.rgb, other_color.rgb)
    w = calc_upper_ratio_limit(other_color.rgb) / 2.0

    upper_rgb = _upper_limit_color(criteria, other_color.rgb, w * 2)
    if upper_rgb:
        return upper_rgb
    (r, sufficient_r) = _calc_brightness_ratio(other_color.rgb, criteria, w)

    satisfying_rgb = _generate_satisfying_color(other_color.rgb, criteria, r, sufficient_r)

    return satisfying_rgb


def _upper_limit_color(criteria, other_rgb, max_ratio):
    limit_rgb = calc_rgb(other_rgb, max_ratio)

    if _exceed_upper_limit(criteria, other_rgb, limit_rgb):
        return limit_rgb

    return None


def _exceed_upper_limit(criteria, other_rgb, limit_rgb):
    other_luminance = checker.relative_luminance(other_rgb)
    other_has_higher_luminance = other_luminance > criteria.fixed_luminance
    sufficient_limit = criteria.has_sufficient_contrast(limit_rgb)
    return other_has_higher_luminance and not sufficient_limit


def _calc_brightness_ratio(other_rgb, criteria, w):
    target_ratio = criteria.target_ratio
    r = w
    sufficient_r = None

    for d in binary_search_width(w, 0.01):
        contrast_ratio = criteria.contrast_ratio(calc_rgb(other_rgb, r))

        if contrast_ratio >= target_ratio:
            sufficient_r = r

        if contrast_ratio == target_ratio:
            break

        r += d if criteria.increment_condition(contrast_ratio) else -d

    return (r, sufficient_r)


def _generate_satisfying_color(other_rgb, criteria, r, sufficient_r):
    level = criteria.level
    nearest = calc_rgb(other_rgb, criteria.round(r))
    satisfying_nearest = criteria.has_sufficient_contrast(nearest)

    if sufficient_r and not satisfying_nearest:
        return calc_rgb(other_rgb, criteria.round(sufficient_r))

    return nearest


def calc_upper_ratio_limit(rgb):
    if rgb == const.rgb.BLACK:
        return 100

    darkest = min(c for c in rgb if c != 0)
    return math.ceil((255.0 / darkest) * 100)
