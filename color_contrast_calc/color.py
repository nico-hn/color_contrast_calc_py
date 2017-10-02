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

    def contrast_ratio_against(self, other_color):
        if not isinstance(other_color, Color):
            return checker.contrast_ratio(self.rgb, other_color)

        other_luminance = other_color.relative_luminance
        return checker.luminance_to_contrast_ratio(self.relative_luminance,
                                                   other_luminance)

    def contrast_level(self, other_color):
        ratio = self.contrast_ratio_against(other_color)
        return checker.ratio_to_level(ratio)

    def is_same_color(self, other_color):
        if isinstance(other_color, Color):
            return self.hex == other_color.hex
        elif isinstance(other_color, tuple):
            return self.hex == utils.rgb_to_hex(other_color)
        elif isinstance(other_color, str):
            return self.hex == utils.normalize_hex(other_color)
