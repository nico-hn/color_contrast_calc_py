import math

def calc_upper_ratio_limit(color):
    if color.is_same_color(color.__class__.BLACK):
        return 100

    darkest = min(filter(lambda c: c != 0, color.rgb))
    return math.ceil((255.0 / darkest) * 100)
