import unittest
from color_contrast_calc.threshold_finder import brightness
from color_contrast_calc.color import Color

class TestBrightness(unittest.TestCase):
    def setup(self):
        pass

    def test_calc_upper_ratio_limit(self):
        color = Color.from_name('black')
        self.assertEqual(brightness.calc_upper_ratio_limit(color), 100)

        color = color.from_name('orange')
        self.assertEqual(brightness.calc_upper_ratio_limit(color), 155)

        color = color.from_name('blueviolet')
        self.assertEqual(brightness.calc_upper_ratio_limit(color), 594)
