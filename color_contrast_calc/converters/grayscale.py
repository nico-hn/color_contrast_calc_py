# https://www.w3.org/TR/filter-effects/#funcdef-grayscale
# https://www.w3.org/TR/filter-effects/#grayscaleEquivalent
# https://www.w3.org/TR/SVG/filters.html#feColorMatrixElement

import numpy as np

from . import rgb_clamp


_CONST_PART = np.array([[0.2126, 0.7152, 0.0722],
                        [0.2126, 0.7152, 0.0722],
                        [0.2126, 0.7152, 0.0722]])

_RATIO_PART = np.array([[0.7874, -0.7152, -0.0722],
                        [-0.2126, 0.2848, -0.0722],
                        [-0.2126, -0.7152, 0.9278]])


def calc_rgb(rgb, s):
    return rgb_clamp((_calc_grayscale(s) * np.array(rgb)).sum(1))


def _calc_grayscale(s):
    r = 1 - min((100, s)) / 100.0
    return _CONST_PART + _RATIO_PART * r
