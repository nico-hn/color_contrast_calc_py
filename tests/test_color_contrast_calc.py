import unittest
import color_contrast_calc
from color_contrast_calc import color_from
from color_contrast_calc import InvalidColorRepresentationError

class TestColorContrastCalc(unittest.TestCase):
    def setUp(self):
        pass

    def test_color(self):
        yellow = color_contrast_calc.color.Color.from_name('yellow')
        black = color_contrast_calc.color.Color.from_name('black')

        contrast_ratio = yellow.contrast_ratio_against(black)
        self.assertAlmostEqual(contrast_ratio, 19.56, 2)

    def test_grayscale(self):
        yellow = color_contrast_calc.color.Color.from_name('yellow')
        orange = color_contrast_calc.color.Color.from_name('orange')

        self.assertEqual(yellow.new_grayscale_color().hex, '#ededed')
        self.assertEqual(orange.new_grayscale_color().hex, '#acacac')

    def test_color_from(self):
        yellow_name = 'yellow'
        yellow_hex = '#ffff00'
        yellow_short_hex = '#ff0'
        yellow_rgb = (255, 255, 0)
        invalid_name = 'imaginaryblue'
        invalid_hex = '#ff00'
        invalid_rgb = (255, 256, 0)

        self.assertEqual(color_from(yellow_name).hex, yellow_hex)
        self.assertEqual(color_from(yellow_hex).hex, yellow_hex)
        self.assertEqual(color_from(yellow_short_hex).hex, yellow_hex)
        self.assertEqual(color_from(yellow_rgb).hex, yellow_hex)

        with self.assertRaises(InvalidColorRepresentationError):
            color_from(invalid_name)
        with self.assertRaises(InvalidColorRepresentationError):
            color_from(invalid_hex)
        with self.assertRaises(InvalidColorRepresentationError):
            color_from(invalid_rgb)
        with self.assertRaises(InvalidColorRepresentationError):
            color_from(0)
