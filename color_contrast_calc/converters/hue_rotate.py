# https://www.w3.org/TR/filter-effects/#funcdef-hue-rotate
# https://www.w3.org/TR/SVG/filters.html#TransferFunctionElementAttributes

import numpy as np

from . import rgb_clamp


CONST_PART = np.array([[0.213, 0.715, 0.072],
                       [0.213, 0.715, 0.072],
                       [0.213, 0.715, 0.072]])

COS_PART = np.array([[0.787, -0.715, -0.072],
                     [-0.213, 0.285, -0.072],
                     [-0.213, -0.715, 0.928]])

SIN_PART = np.array([[-0.213, -0.715, 0.928],
                     [0.143, 0.140, -0.283],
                     [-0.787, 0.715, 0.072]])


def calc_rgb(rgb, deg):
    return rgb_clamp((_calc_rotation(deg) * np.array(rgb)).sum(1))


def _deg_to_rad(deg):
    return np.pi * deg / 180


def _calc_rotation(deg):
    rad = _deg_to_rad(deg)
    cos_part = COS_PART * np.cos(rad)
    sin_part = SIN_PART * np.sin(rad)
    return CONST_PART + cos_part + sin_part
