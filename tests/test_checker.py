import unittest
from color_contrast_calc import checker

_min_contrast = 1.0
_max_contrast = 21.0
_black = (0, 0, 0)
_white = (255, 255, 255)

class TestChecker(unittest.TestCase):
    def setup(self):
        pass

    def test_contrast_ratio(self):
        yellow = (127, 127, 32)

        self.assertEqual(checker.contrast_ratio(_black, _white), _max_contrast)
        self.assertEqual(checker.contrast_ratio(_black, _black), _min_contrast)
        self.assertEqual(checker.contrast_ratio(_white, _white), _min_contrast)
        self.assertAlmostEqual(checker.contrast_ratio(_white, yellow),
                               4.23, 2)
        self.assertAlmostEqual(checker.contrast_ratio('#ffffff', '#7f7f20'),
                               4.23, 2)
        self.assertAlmostEqual(checker.contrast_ratio('#ffffff', yellow),
                               4.23, 2)

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

    def test_ratio_to_level(self):
        self.assertAlmostEqual(checker.ratio_to_level(8), 'AAA')
        self.assertAlmostEqual(checker.ratio_to_level(7), 'AAA')
        self.assertAlmostEqual(checker.ratio_to_level(6), 'AA')
        self.assertAlmostEqual(checker.ratio_to_level(4.5), 'AA')
        self.assertAlmostEqual(checker.ratio_to_level(4), 'A')
        self.assertAlmostEqual(checker.ratio_to_level(3), 'A')
        self.assertAlmostEqual(checker.ratio_to_level(2.9), '-')

    def test_level_to_ratio(self):
        self.assertAlmostEqual(checker.level_to_ratio('AAA'), 7)
        self.assertAlmostEqual(checker.level_to_ratio('AA'), 4.5)
        self.assertAlmostEqual(checker.level_to_ratio('A'), 3)
        self.assertAlmostEqual(checker.level_to_ratio(3), 7)
        self.assertAlmostEqual(checker.level_to_ratio(2), 4.5)
        self.assertAlmostEqual(checker.level_to_ratio(1), 3)
