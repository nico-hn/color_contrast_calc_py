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

    def __str__(self):
        return self.hex

    def contrast_ratio_against(self, other_color):
        if not isinstance(other_color, Color):
            return checker.contrast_ratio(self.rgb, other_color)

        other_luminance = other_color.relative_luminance
        return checker.luminance_to_contrast_ratio(self.relative_luminance,
                                                   other_luminance)

    def contrast_level(self, other_color):
        ratio = self.contrast_ratio_against(other_color)
        return checker.ratio_to_level(ratio)

    def has_sufficient_contrast(self, other_color,
                                level = checker.WCAGLevel.AA):
        ratio = checker.level_to_ratio(level)
        return self.contrast_ratio_against(other_color) >= ratio

    def is_same_color(self, other_color):
        if isinstance(other_color, Color):
            return self.hex == other_color.hex
        elif isinstance(other_color, tuple):
            return self.hex == utils.rgb_to_hex(other_color)
        elif isinstance(other_color, str):
            return self.hex == utils.normalize_hex(other_color)

    def has_min_contrast(self):
        return self.rgb == self.GRAY.rgb

    def has_higher_luminance(self, other_color):
        return self.relative_luminance > other_color.relative_luminance

    def has_same_luminance(self, other_color):
        return self.relative_luminance == other_color.relative_luminance

Color.BLACK = Color((0, 0, 0), 'black')
Color.GRAY = Color((128, 128, 128), 'gray')
Color.WHITE = Color((255, 255, 255), 'white')
