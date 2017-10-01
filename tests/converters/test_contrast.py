import unittest
from color_contrast_calc.converters import contrast

class TestContrast(unittest.TestCase):
    def setup(self):
        pass

    def test_calc_rgb(self):
        yellow = (255, 255, 0)
        yellow2 = (254, 254, 0)
        orange = (255, 165, 0)
        gray = (128, 128, 128)

        self.assertEqual(contrast.calc_rgb(yellow, 100), yellow)
        self.assertEqual(contrast.calc_rgb(yellow2, 100), yellow2)
        self.assertEqual(contrast.calc_rgb(orange, 100), orange)

        self.assertEqual(contrast.calc_rgb(yellow, 0), gray)
        self.assertEqual(contrast.calc_rgb(yellow2, 0), gray)
        self.assertEqual(contrast.calc_rgb(orange, 0), gray)

        self.assertEqual(contrast.calc_rgb(orange, 60), (204, 150, 51))
        self.assertEqual(contrast.calc_rgb(orange, 120), (255, 173, 0))
