'''Module that implements the main logic of the instance method
``Color.find_lightness_threshold``.
'''

from .. import const
from .. import checker
from .. import utils
from .criteria import threshold_criteria, should_scan_darker_side
from . import rgb_with_better_ratio, find_ratio


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
    max_, min_ = _determine_minmax(fixed_rgb, other_rgb, other_hsl[2])
    boundary_rgb = _lightness_boundary_rgb(fixed_rgb, max_, min_, criteria)

    if boundary_rgb:
        return boundary_rgb

    l, sufficient_l = _calc_lightness_ratio(other_hsl, criteria, max_, min_)

    return rgb_with_better_ratio(other_hsl, criteria,
                                 l, sufficient_l, rgb_with_ratio)


def rgb_with_ratio(hsl, ratio):
    if hsl[2] != ratio:
        hsl = hsl[0:2] + (ratio,)

    return utils.hsl_to_rgb(hsl)


def _determine_minmax(fixed_rgb, other_rgb, init_l):
    scan_darker_side = should_scan_darker_side(fixed_rgb, other_rgb)

    return (init_l, 0) if scan_darker_side else (100, init_l)  # (max, min)


def _lightness_boundary_rgb(rgb, max_, min_, criteria):
    black = const.luminance.BLACK
    white = const.luminance.WHITE

    if min_ == 0 and not _has_sufficient_contrast(black, rgb, criteria):
        return const.rgb.BLACK

    if max_ == 100 and not _has_sufficient_contrast(white, rgb, criteria):
        return const.rgb.WHITE

    return None


def _has_sufficient_contrast(fixed_luminance, rgb, criteria):
    luminance = checker.relative_luminance(rgb)
    ratio = checker.luminance_to_contrast_ratio(fixed_luminance, luminance)
    return ratio >= criteria.target_ratio


def _calc_lightness_ratio(other_hsl, criteria, max_, min_):
    return find_ratio(other_hsl, criteria, rgb_with_ratio,
                      (max_ + min_) / 2.0, max_ - min_)
