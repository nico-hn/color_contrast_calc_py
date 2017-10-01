import unittest
from color_contrast_calc.converters import invert

class TestInvert(unittest.TestCase):
    def setup(self):
        pass

    def test_calc_rgb(self):
        yellow = (255, 255, 0)
        blue = (0, 0, 255)
        gray = (128, 128, 128)

        self.assertEqual(invert.calc_rgb(yellow, 0), yellow)
        self.assertEqual(invert.calc_rgb(yellow, 100), blue)
        self.assertEqual(invert.calc_rgb(yellow, 50), gray)
