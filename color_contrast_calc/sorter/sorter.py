import builtins
import operator
import re
from .. import utils
from . import key_types

_HSL_RE = re.compile(r'[hsl]{3}', re.IGNORECASE)
_RGB_COMPONENTS = 'rgb'
_HSL_COMPONENTS = 'hsl'

def sorted(colors, color_order='HSL', key=None):
    key_type = key_types.guess(colors[0], key)
    key_func = compile_sort_key_function(color_order, key_type, key)

    return builtins.sorted(colors, key=key_func)

def compile_sort_key_function(color_order, key_type, key_mapper=None):
    if key_type == key_types.COLOR:
        key_func = compile_color_sort_key_function(color_order)
    elif key_type == key_types.HEX:
        key_func = compile_hex_sort_key_function(color_order)
    else:
        key_func = compile_components_sort_key_function(color_order)

    return compose_key_function(key_func, key_mapper)

def compose_key_function(key_function, key_mapper=None):
    if key_mapper is None:
        return key_function

    def composed_func(color):
        return key_function(key_mapper(color))

    return composed_func

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

def compile_hex_sort_key_function(color_order):
    components_sort_key_func = compile_components_sort_key_function(color_order)

    if is_hsl_order(color_order):
        to_components = utils.hex_to_hsl
    else:
        to_components = utils.hex_to_rgb

    def key_func(hex_code):
        return components_sort_key_func(to_components(hex_code))

    return key_func

def compile_color_sort_key_function(color_order):
    components_sort_key_func = compile_components_sort_key_function(color_order)

    if is_hsl_order(color_order):
        def key_func(color):
            return components_sort_key_func(color.hsl)
    else:
        def key_func(color):
            return components_sort_key_func(color.rgb)

    return key_func
