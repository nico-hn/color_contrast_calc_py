'''Module that implements the main logic of the instance method
``Color.find_brightness_threshold``.
'''

import math

from .. import const
from .. import checker
from ..converters.brightness import calc_rgb
from . import binary_search_width, rgb_with_better_ratio
from .criteria import threshold_criteria


def find(fixed_rgb, other_rgb, level=checker.WCAGLevel.AA):
    """Try to find a color who has a satisfying contrast ratio.

    The color returned by this function will be created by changing the
    brightness of ``other_color``.  Even when a color that satisfies the
    specified level is not found, the function returns a new color
    anyway.
    :param fixed_rgb: An RGB value which remains unchanged
    :type fixed_rgb: (int, int, int)
    :param other_rgb: An RGB value before the adjustment of brightness
    :type other_rgb: (int, int, int)
    :param level: "A", "AA" or "AAA" [optional]
    :type level: str
    :return: New RGB value whose brightness is adjusted from that of
             ``other_color``
    :rtype: (int, int, int)
    """
    criteria = threshold_criteria(level, fixed_rgb, other_rgb)
    w = calc_upper_ratio_limit(other_rgb) / 2.0

    upper_rgb = _upper_limit_color(criteria, other_rgb, w * 2)
    if upper_rgb:
        return upper_rgb

    (r, sufficient_r) = _round_ratios(_find_ratio(other_rgb, criteria, w, w),
                                      criteria)

    return rgb_with_better_ratio(other_rgb, criteria,
                                 r, sufficient_r, calc_rgb)


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


def _find_ratio(other_rgb, criteria, init_ratio, init_width):
    target_ratio = criteria.target_ratio
    r = init_ratio
    sufficient_r = None

    for d in binary_search_width(init_width, 0.01):
        contrast_ratio = criteria.contrast_ratio(calc_rgb(other_rgb, r))

        if contrast_ratio >= target_ratio:
            sufficient_r = r

        if contrast_ratio == target_ratio:
            break

        r += d if criteria.increment_condition(contrast_ratio) else -d

    return (r, sufficient_r)


def _round_ratios(ratios, criteria):
    return tuple(criteria.round(r) if r != None else None for r in ratios)


def calc_upper_ratio_limit(rgb):
    if rgb == const.rgb.BLACK:
        return 100

    darkest = min(c for c in rgb if c != 0)
    return math.ceil((255.0 / darkest) * 100)
