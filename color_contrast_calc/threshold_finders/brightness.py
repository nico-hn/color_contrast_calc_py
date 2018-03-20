'''Module that implements the main logic of the instance method
``Color.find_brightness_threshold``.
'''

import math

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
    :return: New color whose brightness is adjusted from that of
             ``other_color``
    :rtype: Color
    """
    criteria = threshold_criteria(level, fixed_color, other_color)
    w = calc_upper_ratio_limit(other_color) / 2.0

    upper_color = _upper_limit_color(fixed_color, other_color, w * 2, level)
    if upper_color:
        return upper_color
    (r, sufficient_r) = _calc_brightness_ratio(other_color.rgb, criteria, w)

    return _generate_satisfying_color(other_color, criteria, r, sufficient_r)


def _upper_limit_color(fixed_color, other_color, max_ratio, level):
    limit_color = other_color.new_brightness_color(max_ratio)

    if _exceed_upper_limit(fixed_color, other_color, limit_color, level):
        return limit_color

    return None


def _exceed_upper_limit(fixed_color, other_color, limit_color, level):
    other_has_higher_luminance = other_color.has_higher_luminance(fixed_color)
    sufficient_limit = limit_color.has_sufficient_contrast(fixed_color, level)
    return other_has_higher_luminance and not sufficient_limit


def _calc_brightness_ratio(other_rgb, criteria, w):
    target_ratio = criteria.target_ratio
    r = w
    sufficient_r = None

    for d in binary_search_width(w, 0.01):
        contrast_ratio = _calc_contrast_ratio(criteria.fixed_luminance,
                                              other_rgb, r)

        if contrast_ratio >= target_ratio:
            sufficient_r = r

        if contrast_ratio == target_ratio:
            break

        r += d if criteria.increment_condition(contrast_ratio) else -d

    return (r, sufficient_r)


def _generate_satisfying_color(other_color, criteria, r, sufficient_r):
    level = criteria.level
    nearest = other_color.new_brightness_color(criteria.round(r))
    satisfying_nearest = criteria.has_sufficient_contrast(nearest.rgb)

    if sufficient_r and not satisfying_nearest:
        return other_color.new_brightness_color(criteria.round(sufficient_r))

    return nearest


def _calc_contrast_ratio(fixed_luminance, other_rgb, r):
    new_rgb = calc_rgb(other_rgb, r)
    new_luminance = checker.relative_luminance(new_rgb)

    return checker.luminance_to_contrast_ratio(fixed_luminance, new_luminance)


def calc_upper_ratio_limit(color):
    if color.is_same_color(color.__class__.BLACK):
        return 100

    darkest = min(c for c in color.rgb if c != 0)
    return math.ceil((255.0 / darkest) * 100)
