from . import utils
from . import checker
import converters as conv

class Color:
    def __init__(self, rgb, name = None):
        if isinstance(rgb, str):
            self.rgb = utils.hex_to_rgb(rgb)
        else:
            self.rgb = rgb

        self.hex = utils.rgb_to_hex(self.rgb)
        self.name = name or self.hex
        self.relative_luminance = checker.relative_luminance(self.rgb)
