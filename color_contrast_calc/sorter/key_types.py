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
    elif isinstance(key, str):
        return HEX
    else:
        return COMPONENTS
