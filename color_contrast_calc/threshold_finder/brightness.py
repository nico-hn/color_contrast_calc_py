import math
from functools import reduce

def calc_upper_ratio_limit(color):
    if color.is_same_color(color.__class__.BLACK):
        return 100

    darkest = reduce(lambda f, s: f if s == 0 or f < s else s, color.rgb)
    return math.ceil((255.0 / darkest) * 100)
