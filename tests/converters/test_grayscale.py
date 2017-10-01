import unittest
from color_contrast_calc.converters import grayscale

class TestGrayscale(unittest.TestCase):
    def setup(self):
        pass

    def test_calc_rgb(self):
        yellow = (255, 255, 0)
        orange = (255, 165, 0)

        r = 0
        self.assertEqual(grayscale.calc_rgb(yellow, r), yellow)
        self.assertEqual(grayscale.calc_rgb(orange, r), orange)

        r = 100
        self.assertEqual(grayscale.calc_rgb(yellow, r), (237, 237, 237))
        self.assertEqual(grayscale.calc_rgb(orange, r), (172, 172, 172))

        r = 50
        self.assertEqual(grayscale.calc_rgb(yellow, r), (246, 246, 118))
        self.assertEqual(grayscale.calc_rgb(orange, r), (214, 169 ,86))
