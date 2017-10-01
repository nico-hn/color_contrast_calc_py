# https://www.w3.org/TR/filter-effects/#funcdef-saturate
# https://www.w3.org/TR/SVG/filters.html#feColorMatrixElement

import numpy as np
from . import rgb_clamp

_CONST_PART = np.array([[0.213, 0.715, 0.072],
                        [0.213, 0.715, 0.072],
                        [0.213, 0.715, 0.072]])

_SATURATE_PART = np.array([[0.787, -0.715, -0.072],
                           [-0.213, 0.285, -0.072],
                           [-0.213, -0.715, 0.928]])

def calc_rgb(rgb, s):
    return rgb_clamp((_calc_saturation(s) * np.array(rgb)).sum(1))

def _calc_saturation(s):
    return _CONST_PART + _SATURATE_PART * (s / 100.0)
