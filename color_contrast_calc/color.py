from os import path
import json
from itertools import product

from . import utils
from . import checker
from . import converters as conv
from . import threshold_finders


class Color:
    @classmethod
    def from_name(cls, name):
        """Returns an instance of Color for a predefined color name.

        Color names are defined at
        https://www.w3.org/TR/SVG/types.html#ColorKeywords
        :param name: Name of color
        :type name: str
        :return: an instance of Color
        :rtype: Color
        """
        if not name in NAME_TO_COLOR:
            return None

        return NAME_TO_COLOR[name]

    @classmethod
    def from_hex(cls, hex_code):
        """Returns an instance of Color for a hex color code

        :param hex_code: Hex color code such as "#ffff00"
        :type hex_code: str
        :return: an instance of Color
        :rtype: Color
        """
        normalized_hex = utils.normalize_hex(hex_code)
        if normalized_hex in HEX_TO_COLOR:
            return HEX_TO_COLOR[normalized_hex]

        return Color(normalized_hex)

    @classmethod
    def new_from_hsl(cls, hsl, name=None):
        """Creates an instance of Color from an HSL value

        :param name: You can name the color to be created [optional]
        :type name: str
        :param hsl: HSL value represented as a tuple of numbers
        :type hsl: (number, number, number)
        :return: an instance of Color
        :rtype: Color
        """
        return cls(utils.hsl_to_rgb(hsl), name)

    def __init__(self, rgb, name=None):
        """Creates an instance of Color

        :param name: You can name the color to be created.
                     Without this option, the value of normalized hex
                     color code is assigned instead. [optional]
        :type name: str
        :param rgb: RGB value represented as a tuple of integers or
                    hex color code such as "#ffff00"
        :type rgb: str or (int, int, int)
        :return: an instance of Color
        :rtype: Color
        """
        if isinstance(rgb, str):
            self.rgb = utils.hex_to_rgb(rgb)
        else:
            self.rgb = rgb

        self.hex = utils.rgb_to_hex(self.rgb)
        self.name = name or self.hex
        self.relative_luminance = checker.relative_luminance(self.rgb)
        self.__hsl = None
        self.__rgb_code = None

    def __str__(self):
        return self.hex

    @property
    def hsl(self):
        if self.__hsl is None:
            self.__hsl = utils.rgb_to_hsl(self.rgb)

        return self.__hsl

    @property
    def rgb_code(self):
        if  self.__rgb_code is None:
            self.__rgb_code = 'rgb({:d},{:d},{:d})'.format(*self.rgb)

        return self.__rgb_code

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
                                level=checker.WCAGLevel.AA):
        ratio = checker.level_to_ratio(level)
        return self.contrast_ratio_against(other_color) >= ratio

    def is_same_color(self, other_color):
        if isinstance(other_color, Color):
            return self.hex == other_color.hex
        elif isinstance(other_color, tuple):
            return self.hex == utils.rgb_to_hex(other_color)
        elif isinstance(other_color, str):
            return self.hex == utils.normalize_hex(other_color)
        else:
            return False

    def has_max_contrast(self):
        return all(c in (0, 255) for c in self.rgb)

    def has_min_contrast(self):
        return self.rgb == self.GRAY.rgb

    def has_higher_luminance(self, other_color):
        return self.relative_luminance > other_color.relative_luminance

    def has_same_luminance(self, other_color):
        return self.relative_luminance == other_color.relative_luminance

    def is_light_color(self):
        contrast_ratio_against_white = self.contrast_ratio_against(self.WHITE)
        contrast_ratio_against_black = self.contrast_ratio_against(self.BLACK)

        return contrast_ratio_against_white <= contrast_ratio_against_black

    def new_contrast_color(self, ratio, name=None):
        return self.__generate_new_color(conv.contrast, ratio, name)

    def new_brightness_color(self, ratio, name=None):
        return self.__generate_new_color(conv.brightness, ratio, name)

    def new_invert_color(self, ratio=100, name=None):
        return self.__generate_new_color(conv.invert, ratio, name)

    def new_hue_rotate_color(self, degree, name=None):
        return self.__generate_new_color(conv.hue_rotate, degree, name)

    def new_saturate_color(self, ratio, name=None):
        return self.__generate_new_color(conv.saturate, ratio, name)

    def new_grayscale_color(self, ratio=100, name=None):
        return self.__generate_new_color(conv.grayscale, ratio, name)

    def __generate_new_color(self, calc, ratio, name=None):
        new_rgb = calc.calc_rgb(self.rgb, ratio)
        return self.__class__(new_rgb, name)

    def find_brightness_threshold(self, other_color,
                                  level=checker.WCAGLevel.AA):
        if not isinstance(other_color, Color):
            other_color = Color(other_color)

        return threshold_finders.brightness.find(self, other_color, level)

    def find_lightness_threshold(self, other_color,
                                 level=checker.WCAGLevel.AA):
        if not isinstance(other_color, Color):
            other_color = Color(other_color)

        return threshold_finders.lightness.find(self, other_color, level)


_here = path.abspath(path.dirname(__file__))

# named colors: https://www.w3.org/TR/SVG/types.html#ColorKeywords
with open(path.join(_here, 'color_keywords.json')) as f:
    _color_keywords = json.loads(f.read())

NAMED_COLORS = tuple(Color(hex, name) for name, hex in _color_keywords)

NAME_TO_COLOR = {color.name: color for color in NAMED_COLORS}

HEX_TO_COLOR = {color.hex: color for color in NAMED_COLORS}


def _generate_web_safe_colors():
    colors = []
    web_safe_values = [c * 17 for c in range(0, 16, 3)]

    for rgb in [tuple(c) for c in sorted(product(web_safe_values, repeat=3))]:
        hex_code = utils.rgb_to_hex(rgb)
        if hex_code in HEX_TO_COLOR:
            colors.append(HEX_TO_COLOR[hex_code])
        else:
            colors.append(Color(hex_code))

    return tuple(colors)


WEB_SAFE_COLORS = _generate_web_safe_colors()


def hsl_colors(s=100, l=50, h_interval=1):
    hues = range(0, 361, h_interval)
    return tuple(Color.new_from_hsl((h, s, l)) for h in hues)


Color.BLACK = Color.from_name('black')
Color.GRAY = Color.from_name('gray')
Color.WHITE = Color.from_name('white')
