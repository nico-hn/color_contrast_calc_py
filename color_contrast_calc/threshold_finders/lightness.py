'''Module that implements the main logic of the instance method
``Color.find_lightness_threshold``.
'''

from .. import const
from .. import checker
from .. import utils
from .criteria import threshold_criteria, should_scan_darker_side
from . import binary_search_width


def find(fixed_color, other_color, level=checker.WCAGLevel.AA):
    """Try to find a color who has a satisfying contrast ratio.

    The color returned by this function will be created by changing the
    lightness of ``other_color``.  Even when a color that satisfies the
    specified level is not found, the function returns a new color
    anyway.
    :param fixed_color: The color which remains unchanged
    :type fixed_color: Color
    :param other_color: Color before the adjustment of lightness
    :type other_color: Color
    :param level: "A", "AA" or "AAA" [optional]
    :type level: str
    :return: New color whose lightness is adjusted from that of
             ``other_color``
    :rtype: Color
    """
    criteria = threshold_criteria(level, fixed_color, other_color)
    init_l = other_color.hsl[2]
    max_, min_ = _determine_minmax(fixed_color.rgb, other_color.rgb, init_l)

    boundary_color = _lightness_boundary_color(fixed_color, max_, min_, level)

    if boundary_color:
        return boundary_color

    l, sufficient_l = _calc_lightness_ratio(other_color.hsl, criteria,
                                            max_, min_)

    return _generate_satisfying_color(fixed_color, other_color.hsl, criteria,
                                      l, sufficient_l)


def _determine_minmax(fixed_rgb, other_rgb, init_l):
    scan_darker_side = should_scan_darker_side(fixed_rgb, other_rgb)

    return (init_l, 0) if scan_darker_side else (100, init_l)  # (max, min)


def _lightness_boundary_color(color, max_, min_, level):
    color_class = color.__class__
    black = const.rgb.BLACK
    white = const.rgb.WHITE

    if min_ == 0 and not _has_sufficient_contrast(black, color.rgb, level):
        return color_class(black)

    if max_ == 100 and not _has_sufficient_contrast(white, color.rgb, level):
        return color_class(white)

    return None


def _has_sufficient_contrast(fixed_rgb, other_rgb, level):
    target_ratio = checker.level_to_ratio(level)
    ratio = checker.contrast_ratio(fixed_rgb, other_rgb)
    return ratio >= target_ratio


def _calc_lightness_ratio(other_hsl, criteria, max_, min_):
    h, s = other_hsl[0:2]
    l = (max_ + min_) / 2.0
    sufficient_l = None

    for d in binary_search_width(max_ - min_, 0.01):
        contrast_ratio = criteria.contrast_ratio(utils.hsl_to_rgb((h, s, l)))

        if contrast_ratio >= criteria.target_ratio:
            sufficient_l = l

        if contrast_ratio == criteria.target_ratio:
            break

        l += d if criteria.increment_condition(contrast_ratio) else -d

    return (l, sufficient_l)


def _generate_satisfying_color(fixed_color, other_hsl, criteria,
                               l, sufficient_l):
    h, s = other_hsl[0:2]
    level = criteria.level
    nearest = utils.hsl_to_rgb((h, s, l))

    if sufficient_l and not criteria.has_sufficient_contrast(nearest):
        return fixed_color.__class__(utils.hsl_to_rgb((h, s, sufficient_l)))

    return fixed_color.__class__(nearest)
