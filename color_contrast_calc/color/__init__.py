'''Provide Color class that represents specific colors

This module also provides lists of predefined colors represented as
instances of Color class.
'''

from os import path
import json
from itertools import product

from .. import utils
from .. import checker

from ._color import Color
from ._color import NAME_TO_COLOR, HEX_TO_COLOR
from ._color import NAMED_COLORS, WEB_SAFE_COLORS

class InvalidColorRepresentationError(Exception):
    '''Error raised if creating a Color instance with invalid value.

    Attributes:
        expression -- Expression of the value that caused the error.
        message -- Explanation of the error.
    '''
    def __init__(self, expression, message):
        super(InvalidColorRepresentationError, self).__init__(message)
        self.expression = expression


def color_from(color_value, name=None):
    """Return an instance of Color.

    As ``color_value``, you can pass a predefined color name, or
    an RGB value represented as a tuple of integers or a hex code such
    as (255, 255, 0) or "#ffff00".  ``name`` is assigned to the returned
    instance.
    :param color_value: Name of a predefined color, hex color code or
                        RGB value
    :type color_value: str or (int, int, int)
    :param name: Without specifying a name, a color keyword name (if
                 exists) or the value of normalized hex color code is
                 set to self.name [optional]
    :type name: str
    :return: Instance of Color
    :rtype: Color
    """
    default_error_message = 'A color should be given as a tuple or string.'

    if not isinstance(color_value, (str, tuple)):
        raise InvalidColorRepresentationError(color_value,
                                              default_error_message)

    if isinstance(color_value, tuple):
        return _color_from_rgb(color_value, name)

    return _color_from_str(color_value, name)


def from_name(name):
    """Return an instance of Color for a predefined color name.

    Color names are defined at
    https://www.w3.org/TR/SVG/types.html#ColorKeywords
    :param name: Name of color
    :type name: str
    :return: Instance of Color
    :rtype: Color
    """
    normalized_name = name.lower()

    if not normalized_name in NAME_TO_COLOR:
        return None

    return NAME_TO_COLOR[normalized_name]


def from_rgb(rgb, name=None):
    """Return an instance of Color for a hex color code.

    :param rgb: RGB value represented as a tuple of integers such
                such as (255, 255, 0)
    :type rgb: (int, int, int)
    :param name: You can name the color to be created [optional]
    :type name: str
    :return: an instance of Color
    :rtype: Color
    """
    hex_code = utils.rgb_to_hex(rgb)
    if not name and hex_code in HEX_TO_COLOR:
        return HEX_TO_COLOR[hex_code]

    return Color(rgb, name)


def from_hex(hex_code, name=None):
    """Return an instance of Color for a hex color code.

    :param hex_code: Hex color code such as "#ffff00"
    :type hex_code: str
    :param name: You can name the color to be created [optional]
    :type name: str
    :return: an instance of Color
    :rtype: Color
    """
    normalized_hex = utils.normalize_hex(hex_code)
    if not name and normalized_hex in HEX_TO_COLOR:
        return HEX_TO_COLOR[normalized_hex]

    return Color(normalized_hex, name)


def from_hsl(hsl, name=None):
    """Create an instance of Color from an HSL value.

    :param hsl: HSL value represented as a tuple of numbers
    :type hsl: (float, float, float)
    :param name: You can name the color to be created [optional]
    :type name: str
    :return: an instance of Color
    :rtype: Color
    """
    hex_code = utils.hsl_to_hex(hsl)
    if not name and hex_code in HEX_TO_COLOR:
        return HEX_TO_COLOR[hex_code]

    return Color(hex_code, name)


def hsl_colors(s=100, l=50, h_interval=1):
    """Return a list of colors which share the same saturation and
    lightness.

    By default, so-called pure colors are returned.
    :param s:  Ratio of saturation in percentage [optional]
    :type s: float
    :param l: Ratio of lightness in percentage [optional]
    :type l: float
    :param h_interval: Interval of hues in degrees.  By default, it
                       returns 360 hues beginning from red. [optional]
    :type h_interval: int
    :return: List of colors
    :rtype: list of Color
    """
    hues = range(0, 361, h_interval)
    return [from_hsl((h, s, l)) for h in hues]


def _color_from_rgb(rgb_value, name=None):
    error_message = 'An RGB value should be given in form of (r, g, b).'

    if not utils.is_valid_rgb(rgb_value):
        raise InvalidColorRepresentationError(rgb_value, error_message)

    hex_code = utils.rgb_to_hex(rgb_value)

    if not name and hex_code in HEX_TO_COLOR:
        return HEX_TO_COLOR[hex_code]

    return Color(rgb_value, name)


def _color_from_str(color_value, name=None):
    error_message = 'A hex code is in form of "#xxxxxx" where 0 <= x <= f.'

    if color_value in NAME_TO_COLOR:
        return NAME_TO_COLOR[color_value]

    if not utils.is_valid_hex(color_value):
        raise InvalidColorRepresentationError(color_value, error_message)

    hex_code = utils.normalize_hex(color_value)

    if not name and hex_code in HEX_TO_COLOR:
        return HEX_TO_COLOR[hex_code]

    return Color(hex_code, name)
