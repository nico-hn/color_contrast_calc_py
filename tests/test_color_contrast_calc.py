import unittest
import color_contrast_calc

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
