import operator
import re
from . import utils

_HSL_RE = re.compile(r'[hsl]{3}', re.IGNORECASE)
_RGB_COMPONENTS = 'rgb'
_HSL_COMPONENTS = 'hsl'

def is_hsl_order(color_order):
    return _HSL_RE.match(color_order) is not None

def color_component_pos(color_order, ordered_components):
    return tuple(ordered_components.find(c) for c in color_order.lower())

def parse_color_order(color_order):
    if is_hsl_order((color_order)):
        ordered_components = _HSL_COMPONENTS
    else:
        ordered_components = _RGB_COMPONENTS

    pos = color_component_pos(color_order, ordered_components)
    funcs = {}
    for i, ci in enumerate(pos):
        c = color_order[i]
        funcs[ci] = operator.neg if utils.is_uppercase(c) else operator.pos

    return {'pos': pos, 'funcs': funcs}

def compile_components_sort_key_function(color_order):
    order = parse_color_order(color_order)
    component_positions = order['pos']
    funcs = order['funcs']

    def key_func(components):
        return tuple(funcs[i](components[i]) for i in component_positions)

    return key_func
