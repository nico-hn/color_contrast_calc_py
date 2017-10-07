import operator
import re

_HSL_RE = re.compile(r'[hsl]{3}', re.IGNORECASE)

def is_hsl_order(color_order):
    return _HSL_RE.match(color_order) is not None
