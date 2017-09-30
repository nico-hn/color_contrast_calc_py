import unittest
from color_contrast_calc import checker

_min_contrast = 1.0
_max_contrast = 21.0
_black = (0, 0, 0)
_white = (255, 255, 255)

class TestChecker(unittest.TestCase):
    def setup(self):
        pass

    def test_luminance_to_contrast_ratio(self):
        black_l = checker.relative_luminance(_black)
        white_l = checker.relative_luminance(_white)
        yellow_l = checker.relative_luminance((127, 127, 32))
        ratio = checker.luminance_to_contrast_ratio(black_l, white_l)
        black_ratio = checker.luminance_to_contrast_ratio(black_l, black_l)
        white_ratio = checker.luminance_to_contrast_ratio(white_l, white_l)
        yellow_ratio = checker.luminance_to_contrast_ratio(white_l, yellow_l)

        self.assertEqual(ratio, _max_contrast)
        self.assertEqual(black_ratio, _min_contrast)
        self.assertEqual(white_ratio, _min_contrast)
        self.assertAlmostEqual(yellow_ratio, 4.23, 2)