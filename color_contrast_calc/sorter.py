import operator
import re

_HSL_RE = re.compile(r'[hsl]{3}', re.IGNORECASE)
_RGB_COMPONENTS = 'rgb'
_HSL_COMPONENTS = 'hsl'

def is_hsl_order(color_order):
    return _HSL_RE.match(color_order) is not None

def color_component_pos(color_order, ordered_components):
    return tuple(ordered_components.find(c) for c in color_order.lower())
