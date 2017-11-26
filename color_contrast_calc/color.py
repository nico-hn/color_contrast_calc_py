'''Provide Color class that represents specific colors

This module also provides lists of predefined colors represented as
instances of Color class.
'''

from os import path
import json
from itertools import product

from . import utils
from . import checker
from .threshold_finders import brightness as brightness_finder
from .threshold_finders import lightness as lightness_finder
from .converters import brightness as brightness_conv
from .converters import contrast as contrast_conv
from .converters import grayscale as grayscale_conv
from .converters import hue_rotate as hue_rotate_conv
from .converters import invert as invert_conv
from .converters import saturate as saturate_conv


class Color:
    @classmethod
    def from_name(cls, name):
        """Return an instance of Color for a predefined color name.

        Color names are defined at
        https://www.w3.org/TR/SVG/types.html#ColorKeywords
        :param name: Name of color
        :type name: str
        :return: Instance of Color
        :rtype: Color
        """
        normalized_name = name.lower()

        if not normalized_name in NAME_TO_COLOR:
            return None

        return NAME_TO_COLOR[normalized_name]

    @classmethod
    def from_hex(cls, hex_code):
        """Return an instance of Color for a hex color code.

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
        """Create an instance of Color from an HSL value.

        :param hsl: HSL value represented as a tuple of numbers
        :type hsl: (float, float, float)
        :param name: You can name the color to be created [optional]
        :type name: str
        :return: an instance of Color
        :rtype: Color
        """
        return cls(utils.hsl_to_rgb(hsl), name)

    def __init__(self, rgb, name=None):
        """Create an instance of Color.

        :param rgb: RGB value represented as a tuple of integers or
                    hex color code such as "#ffff00"
        :type rgb: str or (int, int, int)
        :param name: You can name the color to be created.
                     Without this option, the value of normalized hex
                     color code is assigned instead. [optional]
        :type name: str
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
        """Return HSL value of the color.

        The value is calculated from the RGB value, so if you create
        the instance by Color.new_from_hsl method, the value used to
        create the color does not necessarily correspond to the value
        of this property.
        :return: HSL value represented as a tuple of numbers
        :rtype: (float, float, float)
        """
        if self.__hsl is None:
            self.__hsl = utils.rgb_to_hsl(self.rgb)

        return self.__hsl

    @property
    def rgb_code(self):
        """Return a string representation of RGB value.

        :return: For example if the color is yellow, the return value
                 is "rgb(255,255,0)".
        :rtype: str
        """
        if  self.__rgb_code is None:
            self.__rgb_code = 'rgb({:d},{:d},{:d})'.format(*self.rgb)

        return self.__rgb_code

    def contrast_ratio_against(self, other_color):
        """Calculate the contrast ratio against another color.

        :param other_color: Another instance of Color, RGB value or
                            hex color code
        :type other_color: Color or (int, int, int) or str
        :return: Contrast ratio
        :rtype: float
        """
        if not isinstance(other_color, Color):
            return checker.contrast_ratio(self.rgb, other_color)

        other_luminance = other_color.relative_luminance
        return checker.luminance_to_contrast_ratio(self.relative_luminance,
                                                   other_luminance)

    def contrast_level(self, other_color):
        """Return the level of contrast ratio defined by WCAG 2.0.

        :param other_color: Another instance of Color, RGB value or
                            hex color code
        :type other_color: Color or (int, int, int) or str
        :return: "A", "AA" or "AAA" if the contrast ratio meets the
                 criteria of WCAG 2.0, otherwise "-"
        :rtype: str
        """
        ratio = self.contrast_ratio_against(other_color)
        return checker.ratio_to_level(ratio)

    def has_sufficient_contrast(self, other_color,
                                level=checker.WCAGLevel.AA):
        """Check if the contrast ratio with another color meets a
        WCAG 2.0 criterion.

        :param other_color: Another instance of Color, RGB value or
                            hex color code
        :type other_color: Color or (int, int, int) or str
        :param level: "A", "AA" or "AAA" [optional]
        :type level: str
        :return: True if the contrast ratio meets the specified level
        :rtype: bool
        """
        ratio = checker.level_to_ratio(level)
        return self.contrast_ratio_against(other_color) >= ratio

    def is_same_color(self, other_color):
        """Check it two colors have the same RGB value.

        :param other_color: Another instance of Color, RGB value or
                            hex color code
        :type other_color: Color or (int, int, int) or str
        :return: True if other_color has the same RGB value
        :rtype: bool
        """
        if isinstance(other_color, Color):
            return self.hex == other_color.hex
        elif isinstance(other_color, tuple):
            return self.hex == utils.rgb_to_hex(other_color)
        elif isinstance(other_color, str):
            return self.hex == utils.normalize_hex(other_color)
        else:
            return False

    def has_max_contrast(self):
        """Check if the color reachs already the max contrast..

        The max contrast in this context means that of colors modified
        by the operation defined at
        https://www.w3.org/TR/filter-effects/#funcdef-contrast
        :return: True if self.new_contrast_color(r) where r is greater
                 than 100 returns the same color as self.
        :rtype: bool
        """
        return all(c in (0, 255) for c in self.rgb)

    def has_min_contrast(self):
        """Check if the color reachs already the min contrast.

        The min contrast in this context means that of colors modified
        by the operation defined at
        https://www.w3.org/TR/filter-effects/#funcdef-contrast
        :return: True if self is the same color as "#808080"
        :rtype: bool
        """
        return self.rgb == self.GRAY.rgb

    def has_higher_luminance(self, other_color):
        """Check if the color has higher luminance than another color.

        :param other_color: Another color
        :type other_color: Color
        :return: True if the relative luminance of self is higher than
                 that of other_color
        :rtype: bool
        """
        return self.relative_luminance > other_color.relative_luminance

    def has_same_luminance(self, other_color):
        """Check if two colors has the same relative luminance.

        :param other_color: Another color
        :type other_color: Color
        :return: True if the relative luminance of self and other_color
                 are same.
        :rtype: bool
        """
        return self.relative_luminance == other_color.relative_luminance

    def is_light_color(self):
        """Check if the contrast ratio against black is higher than
           against white.

        :return: True if the contrast ratio against white is qual to or
                 less than the ratio against black
        :rtype: bool
        """
        contrast_ratio_against_white = self.contrast_ratio_against(self.WHITE)
        contrast_ratio_against_black = self.contrast_ratio_against(self.BLACK)

        return contrast_ratio_against_white <= contrast_ratio_against_black

    def new_contrast_color(self, ratio, name=None):
        """Return a new instance of Color with adjusted contrast.

        :param ratio: Adjustment ratio in percentage
        :type ratio: float
        :param name: You can name the color to be created.
                     Without this option, the value of normalized hex
                     color code is assigned instead. [optional]
        :type name: str
        :return: New color with adjusted contrast
        :rtype: Color
        """
        return self.__generate_new_color(contrast_conv, ratio, name)

    def new_brightness_color(self, ratio, name=None):
        """Return a new instance of Color with adjusted brightness.

        :param ratio: Adjustment ratio in percentage
        :type ratio: float
        :param name: You can name the color to be created.
                     Without this option, the value of normalized hex
                     color code is assigned instead. [optional]
        :type name: str
        :return: New color with adjusted brightness
        :rtype: Color
        """
        return self.__generate_new_color(brightness_conv, ratio, name)

    def new_invert_color(self, ratio=100, name=None):
        """Return an inverted color as an instance of Color.

        :param ratio: Proportion of the conversion in percentage
        :type ratio: float
        :param name: You can name the color to be created.
                     Without this option, the value of normalized hex
                     color code is assigned instead. [optional]
        :type name: str
        :return: New inverted color
        :rtype: Color
        """
        return self.__generate_new_color(invert_conv, ratio, name)

    def new_hue_rotate_color(self, degree, name=None):
        """Return a hue rotation applied color as an instance of Color.

        :param ratio: Degrees of rotation (0 to 360)
        :type ratio: float
        :param name: You can name the color to be created.
                     Without this option, the value of normalized hex
                     color code is assigned instead. [optional]
        :type name: str
        :return: New hue rotation applied color
        :rtype: Color
        """
        return self.__generate_new_color(hue_rotate_conv, degree, name)

    def new_saturate_color(self, ratio, name=None):
        """Return a saturated color as an instance of Color.

        :param ratio: Proprtion of the conversion in percentage
        :type ratio: float
        :param name: You can name the color to be created.
                     Without this option, the value of normalized hex
                     color code is assigned instead. [optional]
        :type name: str
        :return: New saturated color
        :rtype: Color
        """
        return self.__generate_new_color(saturate_conv, ratio, name)

    def new_grayscale_color(self, ratio=100, name=None):
        """Return a grayscale of the original color.

        :param ratio: Conversion ratio in percentage
        :type ratio: float
        :param name: You can name the color to be created.
                     Without this option, the value of normalized hex
                     color code is assigned instead. [optional]
        :type name: str
        :return: New grayscale color
        :rtype: Color
        """
        return self.__generate_new_color(grayscale_conv, ratio, name)

    def __generate_new_color(self, calc, ratio, name=None):
        new_rgb = calc.calc_rgb(self.rgb, ratio)
        return self.__class__(new_rgb, name)

    def find_brightness_threshold(self, other_color,
                                  level=checker.WCAGLevel.AA):
        """Try to find a color who has a satisfying contrast ratio.

        The returned color is gained by modifying the brightness of
        another color.  Even when a color that satisfies the specified
        level is not found, it returns a new color anyway.
        :param other_color: Color before the adjustment of brightness
        :type other_color: Color or (int, int, int) or str
        :param level: "A", "AA" or "AAA" [optional]
        :type level: str
        :return: New color whose brightness is adjusted from that of
                 other_color
        :rtype: Color
        """
        if not isinstance(other_color, Color):
            other_color = Color(other_color)

        return brightness_finder.find(self, other_color, level)

    def find_lightness_threshold(self, other_color,
                                 level=checker.WCAGLevel.AA):
        """Try to find a color who has a satisfying contrast ratio.

        The returned color is gained by modifying the lightness of
        another color.  Even when a color that satisfies the specified
        level is not found, it returns a new color anyway.
        :param other_color: Color before the adjustment of lightness
        :type other_color: Color or (int, int, int) or str
        :param level: "A", "AA" or "AAA" [optional]
        :type level: str
        :return: New color whose brightness is adjusted from that of
                 other_color
        :rtype: Color
        """
        if not isinstance(other_color, Color):
            other_color = Color(other_color)

        return lightness_finder.find(self, other_color, level)


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
    """Return a list of colors which share the same saturation and
    lightness.

    By default, so-called pure colors are returned.
    :param s:  Ratio of saturation in percentage [optional]
    :type s: float
    :param l: Ratio of lightness in percentage [optional]
    :type l: float
    :param h_interval: Interval of hues in degrees.  By default, it
                       returns 360 hues beginning from red. [optional]
    :type h_interval: int
    :return: List of colors
    :rtype: list of Color
    """
    hues = range(0, 361, h_interval)
    return [Color.new_from_hsl((h, s, l)) for h in hues]


Color.BLACK = Color.from_name('black')
Color.GRAY = Color.from_name('gray')
Color.WHITE = Color.from_name('white')
