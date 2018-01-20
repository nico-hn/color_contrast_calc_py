'''Define constants used as a value of argument ``key_type`` of
sorter.compile_sort_key_function().

The constants COLOR, COMPONENTS and HEX correspond respectively to
an instance of Color, an RGB or HSL value represented as a tuple of
numbers and a hex color code represented as a string.
'''

from ..color import Color

COLOR = 'COLOR'
COMPONENTS = 'COMPONENTS'
HEX = 'HEX'


def guess(color, key_mapper=None):
    """Return COLOR, COMPONENTS or HEX when a possible key value is passed.

    :param color: Possible key value
    :type color: Color or (int, int, int) or (float, float, float) or str
    :param key_mapper: Function which retrieves a key value from ``color``,
                       that means ``key_mapper(color)`` returns a key value.
                       [optional]
    :type key_mapper: function or None
    :return: "COLOR", "COMPONENTS" or "HEX"
    :rtype: str
    """
    key = color if key_mapper is None else key_mapper(color)

    if isinstance(key, Color):
        return COLOR
    if isinstance(key, str):
        return HEX

    return COMPONENTS
