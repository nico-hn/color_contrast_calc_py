from ..color import Color

COLOR = 'COLOR'
COMPONENTS = 'COMPONENTS'
HEX = 'HEX'


def guess(color, key_mapper=None):
    key = color if key_mapper is None else key_mapper(color)

    if isinstance(key, Color):
        return COLOR
    elif isinstance(key, str):
        return HEX
    else:
        return COMPONENTS
