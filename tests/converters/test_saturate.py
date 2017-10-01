import unittest
from color_contrast_calc.converters import saturate

class TestSaturate(unittest.TestCase):
    def setup(self):
        pass

    def test_calc_rgb(self):
        yellow = (255, 255, 0)
        orange = (255, 165, 0)
        red = (255, 0, 0)

        r = 100
        self.assertEqual(saturate.calc_rgb(yellow, r), yellow)
        self.assertEqual(saturate.calc_rgb(orange, r), orange)

        r = 0
        self.assertEqual(saturate.calc_rgb(yellow, r), (237, 237, 237))
        self.assertEqual(saturate.calc_rgb(orange, r), (172, 172, 172))

        r = 2357
        self.assertEqual(saturate.calc_rgb(orange, r), red)

        r = 3000
        self.assertEqual(saturate.calc_rgb(orange, r), red)
