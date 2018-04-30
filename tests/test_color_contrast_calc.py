import unittest
import color_contrast_calc
from color_contrast_calc import color_from
from color_contrast_calc.color import InvalidColorRepresentationError

class TestColorContrastCalc(unittest.TestCase):
    def setUp(self):
        pass

    def test_color(self):
        yellow = color_contrast_calc.color.from_name('yellow')
        black = color_contrast_calc.color.from_name('black')

        contrast_ratio = yellow.contrast_ratio_against(black)
        self.assertAlmostEqual(contrast_ratio, 19.56, 2)

    def test_grayscale(self):
        yellow = color_contrast_calc.color.from_name('yellow')
        orange = color_contrast_calc.color.from_name('orange')

        self.assertEqual(yellow.with_grayscale().hex, '#ededed')
        self.assertEqual(orange.with_grayscale().hex, '#acacac')

    def test_color_from(self):
        yellow_name = 'yellow'
        yellow_hex = '#ffff00'
        yellow_short_hex = '#ff0'
        yellow_rgb = (255, 255, 0)
        invalid_name = 'imaginaryblue'
        invalid_hex = '#ff00'
        invalid_rgb = (255, 256, 0)
        invalid_type = [255, 255, 0]
        unnamed_hex = '#767676'
        unnamed_rgb = (118, 118, 118)
        unnamed_gray = 'unnamed_gray'

        self.assertEqual(color_from(yellow_name).hex, yellow_hex)
        self.assertEqual(color_from(yellow_hex).hex, yellow_hex)
        self.assertEqual(color_from(yellow_short_hex).hex, yellow_hex)
        self.assertEqual(color_from(yellow_rgb).hex, yellow_hex)

        self.assertEqual(color_from(unnamed_hex, unnamed_gray).rgb,
                         unnamed_rgb)
        self.assertEqual(color_from(unnamed_hex, unnamed_gray).name,
                         unnamed_gray)
        self.assertEqual(color_from(unnamed_rgb, unnamed_gray).hex,
                         unnamed_hex)
        self.assertEqual(color_from(unnamed_rgb, unnamed_gray).name,
                         unnamed_gray)

        with self.assertRaises(InvalidColorRepresentationError):
            color_from(invalid_name)
        with self.assertRaises(InvalidColorRepresentationError):
            color_from(invalid_hex)
        with self.assertRaises(InvalidColorRepresentationError):
            color_from(invalid_rgb)
        with self.assertRaises(InvalidColorRepresentationError):
            color_from(invalid_type)
        with self.assertRaises(InvalidColorRepresentationError):
            color_from(0)

        yellow = color_from(yellow_rgb)
        named_yellow = color_from(yellow_rgb, 'named_yellow')
        self.assertEqual(yellow.name, 'yellow')
        self.assertEqual(named_yellow.name, 'named_yellow')

        yellow = color_from('#ff0')
        named_yellow = color_from('#ff0', 'named_yellow')
        long_yellow = color_from('#ffff00', 'long_yellow')
        self.assertEqual(yellow.name, 'yellow')
        self.assertEqual(named_yellow.name, 'named_yellow')
        self.assertEqual(long_yellow.name, 'long_yellow')
