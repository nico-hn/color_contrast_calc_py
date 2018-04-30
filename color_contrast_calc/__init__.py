'''Utility for finding WCAG 2.0 compliant color contrasts.

Under the top-level package, the following sub-modules are defined.

*utils*
    Provide methods to convert hex color codes to RGB/HSL values and
    vice versa.
*checker*
    Provide methods to check the contrast ratio of given two colors.
*converters*
    Provide methods to convert certin color properties such as
    brightness or saturation.
*threshold_finders*
    Provide methods to create a color with a color contrast that meets
    a WCAG 2.0 success criterion.
*sorter*
    Provide methods to sort colors in a specified order.  You can choose
    the sorting precedence of HSL/RGB components.
*color*
    Provide a ``Color`` class that will ease the manipulation of colors.
    For obtaining an instance of ``Color``, you may use a factory method
    ``color_contrast_calc.color_from()``.
'''

from . import utils
from .color import Color
from .color import color_from
