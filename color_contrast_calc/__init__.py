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

    As ``color_value``, you can pass a predefined name of color or,
    a RGB value represented as a tuple of integers or a hex code such
    as (255, 255, 0) or "#ffff00".  ``name`` is assigned to the returned
    instance if it does not have a name already assigned.
    :param color_value: Name of a predefined color or RGB value
    :type color_value: str or (int, int, int)
    :param name: Unless the instance has predefined name, the passed
                 name is set to self.name [optional]
    :type name: str
    :return: Instance of Color
    :rtype: Color
    """
    default_error_message = 'A color should be given as a tuple or string.'

    if not isinstance(color_value, str) and not isinstance(color_value, tuple):
        raise InvalidColorRepresentationError(color_value,
                                              default_error_message)

    if isinstance(color_value, tuple):
        return _color_from_rgb(color_value, name)

    return _color_from_str(color_value, name)


def _color_from_rgb(color_value, name=None):
    rgb_error_message = 'A RGB value should be given in form of (r, g, b).'

    if utils.is_valid_rgb(color_value):
        return Color(color_value, name)
    else:
        raise InvalidColorRepresentationError(color_value,
                                              rgb_error_message)


def _color_from_str(color_value, name=None):
    hex_error_message = 'A hex code is in form of "#xxxxxx" where 0 <= x <= f.'

    if color_value in _NAME_TO_COLOR:
        return _NAME_TO_COLOR[color_value]

    if utils.is_valid_hex(color_value):
        hex_code = utils.normalize_hex(color_value)
    else:
        raise InvalidColorRepresentationError(color_value,
                                              hex_error_message)

    predefined_hex = hex_code in _HEX_TO_COLOR
    return _HEX_TO_COLOR[hex_code] if predefined_hex else Color(hex_code, name)
