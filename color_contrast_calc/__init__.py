from . import utils
from .color import Color
from .color import NAME_TO_COLOR as _NAME_TO_COLOR
from .color import HEX_TO_COLOR as _HEX_TO_COLOR

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


def _color_from_rgb(rgb_value, name=None):
    error_message = 'An RGB value should be given in form of (r, g, b).'

    if not utils.is_valid_rgb(rgb_value):
        raise InvalidColorRepresentationError(rgb_value, error_message)

    hex_code = utils.rgb_to_hex(rgb_value)

    if not name and hex_code in _HEX_TO_COLOR:
        return _HEX_TO_COLOR[hex_code]

    return Color(rgb_value, name)


def _color_from_str(color_value, name=None):
    error_message = 'A hex code is in form of "#xxxxxx" where 0 <= x <= f.'

    if color_value in _NAME_TO_COLOR:
        return _NAME_TO_COLOR[color_value]

    if not utils.is_valid_hex(color_value):
        raise InvalidColorRepresentationError(color_value, error_message)

    hex_code = utils.normalize_hex(color_value)

    if not name and hex_code in _HEX_TO_COLOR:
        return _HEX_TO_COLOR[hex_code]

    return Color(hex_code, name)
