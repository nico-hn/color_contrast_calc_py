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
