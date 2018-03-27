'''Module that implements the main logic of the instance method
``Color.find_lightness_threshold``.
'''

from .. import const
from .. import checker
from .. import utils
from .criteria import threshold_criteria, should_scan_darker_side
from . import binary_search_width


def find(fixed_rgb, other_rgb, level=checker.WCAGLevel.AA):
    """Try to find a color who has a satisfying contrast ratio.

    The color returned by this function will be created by changing the
    lightness of ``other_color``.  Even when a color that satisfies the
    specified level is not found, the function returns a new color
    anyway.
    :param fixed_rgb: An RGB value which remains unchanged
    :type fixed_rgb: (int, int, int)
    :param other_rgb: An RGB value before the adjustment of lightness
    :type other_rgb: (int, int, int)
    :param level: "A", "AA" or "AAA" [optional]
    :type level: str
    :return: New RGB value whose lightness is adjusted from that of
             ``other_color``
    :rtype: (int, int, int)
    """
    criteria = threshold_criteria(level, fixed_rgb, other_rgb)
    other_hsl = utils.rgb_to_hsl(other_rgb)
    init_l = other_hsl[2]
    max_, min_ = _determine_minmax(fixed_rgb, other_rgb, init_l)
    boundary_rgb = _lightness_boundary_rgb(fixed_rgb, max_, min_, level)

    if boundary_rgb:
        return boundary_rgb

    l, sufficient_l = _calc_lightness_ratio(other_hsl, criteria, max_, min_)

    return _generate_satisfying_rgb(other_hsl, criteria, l, sufficient_l)


def _determine_minmax(fixed_rgb, other_rgb, init_l):
    scan_darker_side = should_scan_darker_side(fixed_rgb, other_rgb)

    return (init_l, 0) if scan_darker_side else (100, init_l)  # (max, min)


def _lightness_boundary_rgb(rgb, max_, min_, level):
    black = const.rgb.BLACK
    white = const.rgb.WHITE

    if min_ == 0 and not _has_sufficient_contrast(black, rgb, level):
        return black

    if max_ == 100 and not _has_sufficient_contrast(white, rgb, level):
        return white

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


def _generate_satisfying_rgb(other_hsl, criteria, l, sufficient_l):
    h, s = other_hsl[0:2]
    nearest = utils.hsl_to_rgb((h, s, l))

    if sufficient_l and not criteria.has_sufficient_contrast(nearest):
        return utils.hsl_to_rgb((h, s, sufficient_l))

    return nearest
