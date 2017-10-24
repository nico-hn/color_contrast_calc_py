'''Utility functions that provide basic operations on colors

This module provides basic operations on colors given as RGB values
(including their hex code presentations) or HSL values.
'''

from functools import reduce
from numbers import Number
import re

_HEX_RE = re.compile(r'\A#?[0-9a-f]{3}([0-9a-f]{3})?\Z', re.IGNORECASE)


def hex_to_rgb(hex_code):
    """Convert a hex color code string to a RGB value.

    :param hex_code: Hex color code such as "#ffff00"
    :type hex_code: str
    :return: RGB value represented as a tuple of integers
    :rtype: (int, int, int)
    """
    hex_part = _remove_head_sharp(hex_code)

    if len(hex_part) == 3:
        return tuple(int(c, 16) * 17 for c in hex_part)
    elif len(hex_part) == 6:
        primaries = (hex_part[i:(i+2)] for i in (0, 2, 4))
        return tuple(int(c, 16) for c in primaries)

    return None


def rgb_to_hex(rgb):
    """Convert a RGB value to a hex color code.

    :param rgb: RGB value represented as a tuple of integers
    :type rgb: (int, int, int)
    :return: Hex color code such as "#ffff00"
    :rtype: str
    """
    return '#{:02x}{:02x}{:02x}'.format(*rgb)


def normalize_hex(code, prefix=True):
    """Normalize a hex color code to a 6 digits, lowercased one.

    :param code: Hex color code such as "#ffff00", "#ff0" or "FFFF00"
    :type code: str
    :param prefix: If set to False, "#" at the head of result is
                   removed [optional]
    :type prefix: bool
    :return: 6-digit hexadecimal string in lowercase, with/without
             leading "#" depending on the value of prefix
    :rtype: str
    """
    if len(code) < 6:
        hex_part = _remove_head_sharp(code)
        code = ''.join(c * 2 for c in hex_part)

    lowered = code.lower()

    if prefix == lowered.startswith('#'):
        return lowered

    return '#' + lowered if prefix else lowered[1:]


# https://www.w3.org/TR/css3-color/#hsl-color

def hsl_to_rgb(hsl):
    """Convert HSL value to RGB value.

    :param hsl: HSL value represented as a tuple of numbers
    :type hsl: (float, float, float)
    :return: RGB value represented as a tuple of integers
    :rtype: (int, int, int)
    """
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
    """Convert HSL value to hex color code.

    :param hsl: HSL value represented as a tuple of numbers
    :type hsl: (float, float, float)
    :return: Hex color code such as "#ffff00"
    :rtype: str
    """
    return rgb_to_hex(hsl_to_rgb(hsl))


# References:
# Agoston, Max K. (2005).
# "Computer Graphics and Geometric Modeling: Implementation and Algorithms".
# London: Springer
#
# https://accessibility.kde.org/hsl-adjusted.php#hue

def rgb_to_hsl(rgb):
    """Convert RGB value to HSL value.

    :param hsl: RGB value represented as a tuple of integers
    :type hsl: (int, int, int)
    :return: HSL value represented as a tuple of numbers
    :rtype: (float, float, float)
    """
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
    """Convert hex color code to HSL value.

    :param hsl: Hex color code such as "#ffff00"
    :type hsl: str
    :return: HSL value represented as a tuple of numbers
    :rtype: (float, float, float)
    """
    return rgb_to_hsl(hex_to_rgb(hex_code))


def is_valid_rgb(rgb):
    """Check if a given tuple is a valid representation of RGB color.

    :param rgb: RGB value represented as a tuple of integers
    :type rgb: (int, int, int)
    :return: True if a valid RGB value is passed
    :rtype: bool
    """
    return len(rgb) == 3 and all(_valid_rgb_component(c) for c in rgb)


def _valid_rgb_component(component):
    return isinstance(component, int) and component >= 0 and component <= 255


def is_valid_hsl(hsl):
    """Check if a given tuple is a valid representation of HSL color.

    :param hsl: HSL value represented as a tuple of numbers
    :type hsl: (float, float, float)
    :return: True if a valid HSL value is passed
    :rtype: bool
    """
    if len(hsl) != 3:
        return False

    for (i, u) in enumerate((360, 100, 100)):
        c = hsl[i]

        if not isinstance(c, Number) or c < 0 or c > u:
            return False

    return True


def is_valid_hex(hex_code):
    """Check if a given string is a valid representation of RGB color.

    :param hex_code: RGB value in hex color code such as "#ffff00"
    :type hex_code: str
    :return: True if a vaild hex color code is passed
    :rtype: bool
    """
    return _HEX_RE.match(hex_code) is not None


def is_same_hex_color(hex1, hex2):
    """Check if given two hex color codes represent a same color.

    :param hex1: RGB value in hex color code such as "#ffff00",
                 "#ffff00", "#FFFF00" or "#ff0"
    :type hex1: str
    :param hex2: RGB value in hex color code such as "#ffff00",
                 "#ffff00", "#FFFF00" or "#ff0"
    :type hex2: str
    :return: True if given two colors are same
    :rtype: bool
    """
    return normalize_hex(hex1) == normalize_hex(hex2)


def is_uppercase(string):
    """Check if a given string is consists of uppercase letters.

    :param string: string to be checked
    :type string: str
    :return: True if letters in the passed string are all in uppercase.
    :rtype: bool
    """
    return string == string.upper()
