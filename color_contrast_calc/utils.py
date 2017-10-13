# Utility functions that provide basic operations on colors given as
# color codes.

from functools import reduce
from numbers import Number
import re

_HEX_RE = re.compile(r'\A#?[0-9a-f]{3}([0-9a-f]{3})?\Z', re.IGNORECASE)


def hex_to_rgb(hex_code):
    hex_part = _remove_head_sharp(hex_code)

    if len(hex_part) == 3:
        return tuple(int(c, 16) * 17 for c in hex_part)
    elif len(hex_part) == 6:
        primaries = (hex_part[i:(i+2)] for i in (0, 2, 4))
        return tuple(int(c, 16) for c in primaries)


def rgb_to_hex(rgb):
    return '#{:02x}{:02x}{:02x}'.format(*rgb)


def normalize_hex(code, prefix=True):
    if len(code) < 6:
        hex_part = _remove_head_sharp(code)
        code = ''.join(c * 2 for c in hex_part)

    lowered = code.lower()

    if prefix == lowered.startswith('#'):
        return lowered

    return '#' + lowered if prefix else lowered[1:]


# https://www.w3.org/TR/css3-color/#hsl-color

def hsl_to_rgb(hsl):
    h, s, l = (c / u for (c, u) in zip(hsl, (360.0, 100.0, 100.0)))

    m2 = l * (s + 1) if l <= 0.5 else l + s - l * s
    m1 = l * 2 - m2

    adjusted_h = (h + 1 / 3.0, h, h - 1 / 3.0)
    return tuple(round(_hue_to_rgb(m1, m2, ah) * 255) for ah in adjusted_h)


def _hue_to_rgb(m1, m2, h):
    if h < 0:
        h += 1
    if h > 1:
        h -= 1
    if h * 6 < 1:
        return m1 + (m2 - m1) * h * 6
    if h * 2 < 1:
        return m2
    if h * 3 < 2:
        return m1 + (m2 - m1) * (2 / 3.0 - h) * 6
    return m1


def _remove_head_sharp(hex_code):
    if hex_code.startswith('#'):
        return hex_code[1:]

    return hex_code


def hsl_to_hex(hsl):
    return rgb_to_hex(hsl_to_rgb(hsl))


# References:
# Agoston, Max K. (2005).
# "Computer Graphics and Geometric Modeling: Implementation and Algorithms".
# London: Springer
#
# https://accessibility.kde.org/hsl-adjusted.php#hue

def rgb_to_hsl(rgb):
    return (_rgb_to_hue(rgb),
            _rgb_to_saturation(rgb) * 100,
            _rgb_to_lightness(rgb) * 100)


def _rgb_to_lightness(rgb):
    return (max(rgb) + min(rgb)) / 510.0


def _rgb_to_saturation(rgb):
    min_c = min(rgb)
    max_c = max(rgb)

    if min_c == max_c:
        return 0

    d = float(max_c - min_c)

    if _rgb_to_lightness(rgb) <= 0.5:
        return d / (max_c + min_c)
    else:
        return d / (510 - max_c - min_c)


def _rgb_to_hue(rgb):
    min_c = min(rgb)
    max_c = max(rgb)

    if min_c == max_c:
        return 0

    d = float(max_c - min_c)

    mi = reduce(lambda m, c: m if rgb[m] > c[1] else c[0], enumerate(rgb), 0)
    h = mi * 120 + (rgb[(mi + 1) % 3] - rgb[(mi + 2) % 3]) * 60 / d

    return h + 360 if h < 0 else h


def hex_to_hsl(hex_code):
    return rgb_to_hsl(hex_to_rgb(hex_code))


def is_valid_rgb(rgb):
    return len(rgb) == 3 and all(_valid_rgb_component(c) for c in rgb)


def _valid_rgb_component(component):
    return isinstance(component, int) and component >= 0 and component <= 255


def is_valid_hsl(hsl):
    if len(hsl) != 3:
        return False

    for (i, u) in enumerate((360, 100, 100)):
        c = hsl[i]

        if not isinstance(c, Number) or c < 0 or c > u:
            return False

    return True


def is_valid_hex(hex_code):
    return _HEX_RE.match(hex_code) is not None


def is_same_hex_color(hex1, hex2):
    return normalize_hex(hex1) == normalize_hex(hex2)


def is_uppercase(string):
    return string == string.upper()
