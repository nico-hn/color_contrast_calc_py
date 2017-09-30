# Utility to check properties of given colors

from . import utils

def relative_luminance(rgb):
    if isinstance(rgb, str):
        rgb = utils.hex_to_rgb(rgb)

    (r, g, b) = map(lambda c: _tristimulus_value(c), rgb)
    return r * 0.2126 + g  * 0.7152 + b * 0.0722

def _tristimulus_value(primary_color):
    base = 255
    s = float(primary_color) / base

    if s <= 0.03928:
        return s / 12.92
    else:
        return pow((s + 0.055) / 1.055, 2.4)

def contrast_ratio(color1, color2):
    return luminance_to_contrast_ratio(relative_luminance(color1),
                                       relative_luminance(color2))

def luminance_to_contrast_ratio(luminance1, luminance2):
    (l1, l2) = sorted((luminance1, luminance2), reverse = True)
    return (l1 + 0.05) / (l2 + 0.05)
