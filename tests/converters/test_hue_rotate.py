import unittest
from color_contrast_calc.converters import hue_rotate

class TestHueRotate(unittest.TestCase):
    def setup(self):
        pass

    def test_calc_rgb(self):
        yellow = (255, 255, 0)
        orange = (255, 165, 0)
        blue = (0, 0, 255)

        deg = 0
        self.assertEqual(hue_rotate.calc_rgb(yellow, deg), yellow)
        self.assertEqual(hue_rotate.calc_rgb(blue, deg), blue)
        self.assertEqual(hue_rotate.calc_rgb(orange, deg), orange)

        deg = 360
        self.assertEqual(hue_rotate.calc_rgb(yellow, deg), yellow)
        self.assertEqual(hue_rotate.calc_rgb(blue, deg), blue)
        self.assertEqual(hue_rotate.calc_rgb(orange, deg), orange)

        deg = 180
        self.assertEqual(hue_rotate.calc_rgb(yellow, deg), (218, 218, 255))
        self.assertEqual(hue_rotate.calc_rgb(blue, deg), (37, 37, 0))
        self.assertEqual(hue_rotate.calc_rgb(orange, deg), (90, 180, 255))

        deg = 90
        self.assertEqual(hue_rotate.calc_rgb(yellow, deg), (0, 255, 218))
        self.assertEqual(hue_rotate.calc_rgb(blue, deg), (255, 0, 37))
        self.assertEqual(hue_rotate.calc_rgb(orange, deg), (0, 232, 90))
