import unittest
from color_contrast_calc.color import Color

class TestColor(unittest.TestCase):
    def setup(self):
        pass

    def test_propertyies(self):
        yellow_rgb = (255, 255, 0)
        yellow_hex = '#ffff00'
        yellow_short_hex = '#ff0'
        yellow_name = 'yellow'
        yellow_hsl = (60, 100, 50)

        yellow = Color(yellow_rgb, yellow_name)
        self.assertEqual(yellow.rgb, yellow_rgb)
        self.assertEqual(yellow.hex, yellow_hex)
        self.assertEqual(yellow.name, yellow_name)
        self.assertAlmostEqual(yellow.relative_luminance, 0.9278)

        yellow = Color(yellow_hex, yellow_name)
        yellow_short = Color(yellow_short_hex, yellow_name)
        self.assertEqual(yellow.rgb, yellow_rgb)
        self.assertEqual(yellow.hex, yellow_hex)
        self.assertAlmostEqual(yellow.relative_luminance, 0.9278)
        self.assertEqual(yellow_short.rgb, yellow_rgb)
        self.assertEqual(yellow_short.hex, yellow_hex)
        self.assertAlmostEqual(yellow_short.relative_luminance, 0.9278)

        yellow = Color(yellow_rgb)
        self.assertEqual(yellow.rgb, yellow_rgb)
        self.assertEqual(yellow.hex, yellow_hex)
        self.assertEqual(yellow.name, yellow_hex)

    def test_contrast_ratio_against(self):
        color = Color((127, 127, 32))
        white = Color((255, 255, 255))
        expected_ratio = 4.23

        ratio = color.contrast_ratio_against(white.rgb)
        self.assertAlmostEqual(ratio, expected_ratio, 2)

        ratio = color.contrast_ratio_against(white.rgb)
        self.assertAlmostEqual(ratio, expected_ratio, 2)

        ratio = color.contrast_ratio_against(white)
        self.assertAlmostEqual(ratio, expected_ratio, 2)

    def test_contrast_level(self):
        white = Color((255, 255, 255))
        black = Color((0, 0, 0))
        orange = Color((255, 165, 0))
        royalblue = Color((65,105, 225))
        steelblue = Color((70, 130, 180))

        self.assertEqual(white.contrast_level(black), 'AAA')
        self.assertEqual(royalblue.contrast_level(white), 'AA')
        self.assertEqual(steelblue.contrast_level(white), 'A')
        self.assertEqual(orange.contrast_level(white), '-')
