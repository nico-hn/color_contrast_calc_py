import unittest
from color_contrast_calc.converters import brightness

class TestBrightness(unittest.TestCase):
    def setup(self):
        pass

    def test_calc_rgb(self):
        yellow = (255, 255, 0)
        yellow2 = (254, 254, 0)
        orange = (255, 165, 0)
        gray = (128, 128, 128)
        black = (0, 0, 0)
        white = (255, 255, 255)

        self.assertEqual(brightness.calc_rgb(yellow, 100), yellow)
        self.assertEqual(brightness.calc_rgb(yellow2, 100), yellow2)
        self.assertEqual(brightness.calc_rgb(orange, 100), orange)

        self.assertEqual(brightness.calc_rgb(yellow, 0), black)
        self.assertEqual(brightness.calc_rgb(yellow2, 0), black)
        self.assertEqual(brightness.calc_rgb(orange, 0), black)

        self.assertEqual(brightness.calc_rgb(orange, 60), (153,99, 0))
        self.assertEqual(brightness.calc_rgb(orange, 120), (255, 198, 0))

        self.assertEqual(brightness.calc_rgb(white, 120), white)
        self.assertEqual(brightness.calc_rgb(yellow, 120), yellow)

