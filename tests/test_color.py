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

    def test_str(self):
        yellow = Color((255, 255, 0), 'yellow')
        yellow_rgb = '#ffff00'
        self.assertEqual(str(yellow), yellow_rgb)

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

    def test_has_sufficient_contrast(self):
        black = Color((0, 0, 0))
        white  = Color((255, 255, 255))
        orange = Color((255, 165, 0))
        blueviolet = Color((138, 43, 226))

        self.assertTrue(black.has_sufficient_contrast(white))
        self.assertTrue(black.has_sufficient_contrast(white, 'A'))
        self.assertTrue(black.has_sufficient_contrast(white, 'AA'))
        self.assertTrue(black.has_sufficient_contrast(white, 'AAA'))

        self.assertFalse(orange.has_sufficient_contrast(white))
        self.assertFalse(orange.has_sufficient_contrast(white, 'A'))
        self.assertFalse(orange.has_sufficient_contrast(white, 'AA'))
        self.assertFalse(orange.has_sufficient_contrast(white, 'AAA'))

        self.assertTrue(orange.has_sufficient_contrast(blueviolet, 'A'))
        self.assertFalse(orange.has_sufficient_contrast(blueviolet))
        self.assertFalse(orange.has_sufficient_contrast(blueviolet, 'AA'))
        self.assertFalse(orange.has_sufficient_contrast(blueviolet, 'AAA'))

        self.assertTrue(white.has_sufficient_contrast(blueviolet))
        self.assertTrue(white.has_sufficient_contrast(blueviolet, 'AA'))
        self.assertFalse(white.has_sufficient_contrast(blueviolet, 'AAA'))

    def test_is_same_color(self):
        yellow_rgb = (255, 255, 0)
        yellow_hex = '#ffff00'
        yellow_short_hex = '#ff0'
        white_rgb = (255, 255, 255)
        yellow = Color(yellow_rgb, 'yellow')
        yellow2 = Color(yellow_rgb, 'yellow2')
        white = Color(white_rgb)

        self.assertEqual(yellow.hex, yellow2.hex)
        self.assertTrue(yellow.is_same_color(yellow2))

        self.assertNotEqual(yellow.hex, white.hex)
        self.assertFalse(yellow.is_same_color(white))

        self.assertTrue(yellow.is_same_color(yellow_hex))
        self.assertTrue(yellow.is_same_color(yellow_short_hex))
        self.assertFalse(white.is_same_color(yellow_short_hex))
        self.assertFalse(white.is_same_color(yellow_short_hex))

        self.assertTrue(yellow.is_same_color(yellow_rgb))
        self.assertFalse(white.is_same_color(yellow_rgb))

    def test_has_max_contrast(self):
        self.assertTrue(Color((255, 255, 0)).has_max_contrast())
        self.assertFalse(Color((255, 165, 0)).has_max_contrast())

    def test_has_min_contrast(self):
        gray = Color((128, 128, 128))
        orange = Color((255, 165, 0))

        self.assertTrue(gray.has_min_contrast())
        self.assertFalse(orange.has_min_contrast())

    def test_has_higher_luminance(self):
        yellow = Color((255, 255, 0))
        orange = Color((255, 165, 0))

        self.assertTrue(yellow.has_higher_luminance(orange))
        self.assertFalse(orange.has_higher_luminance(yellow))
        self.assertFalse(orange.has_higher_luminance(orange))

    def test_has_same_luminance(self):
        yellow = Color((255, 255, 0))
        orange = Color((255, 165, 0))

        self.assertTrue(yellow.has_same_luminance(yellow))
        self.assertFalse(orange.has_same_luminance(yellow))

    def test_is_light_color(self):
        self.assertTrue(Color((118, 118, 118)).is_light_color())
        self.assertFalse(Color((117, 117, 117)).is_light_color())

    def test_new_contrast_color(self):
        yellow = Color((255, 255, 0))
        orange = Color((255, 165, 0))
        lime = Color((0, 255, 0))
        blue = Color((0, 0, 255))
        white = Color((255, 255, 255))
        black = Color((0, 0, 0))
        neutral_gray = Color((118, 118, 118))
        gray_rgb = (128, 128, 128)

        self.assertEqual(yellow.new_contrast_color(100).rgb, yellow.rgb)
        self.assertEqual(orange.new_contrast_color(100).rgb, orange.rgb)
        self.assertEqual(lime.new_contrast_color(100).rgb, lime.rgb)
        self.assertEqual(blue.new_contrast_color(100).rgb, blue.rgb)

        self.assertEqual(yellow.new_contrast_color(0).rgb, gray_rgb)
        self.assertEqual(orange.new_contrast_color(0).rgb, gray_rgb)
        self.assertEqual(lime.new_contrast_color(0).rgb, gray_rgb)
        self.assertEqual(blue.new_contrast_color(0).rgb, gray_rgb)
        self.assertEqual(white.new_contrast_color(0).rgb, gray_rgb)
        self.assertEqual(black.new_contrast_color(0).rgb, gray_rgb)
        self.assertEqual(neutral_gray.new_contrast_color(0).rgb, gray_rgb)

        self.assertEqual(orange.new_contrast_color(60).rgb, (204, 150, 51))
        self.assertEqual(orange.new_contrast_color(120).rgb, (255, 173, 0))

    def test_new_brightness_color(self):
        yellow = Color((255, 255, 0))
        orange = Color((255, 165, 0))
        lime = Color((0, 255, 0))
        blue = Color((0, 0, 255))
        white = Color((255, 255, 255))
        black = Color((0, 0, 0))

        self.assertEqual(yellow.new_brightness_color(100).rgb, yellow.rgb)
        self.assertEqual(orange.new_brightness_color(100).rgb, orange.rgb)
        self.assertEqual(lime.new_brightness_color(100).rgb, lime.rgb)
        self.assertEqual(blue.new_brightness_color(100).rgb, blue.rgb)

        self.assertEqual(yellow.new_brightness_color(0).rgb, black.rgb)
        self.assertEqual(orange.new_brightness_color(0).rgb, black.rgb)
        self.assertEqual(lime.new_brightness_color(0).rgb, black.rgb)
        self.assertEqual(blue.new_brightness_color(0).rgb, black.rgb)

        self.assertEqual(white.new_brightness_color(120).rgb, white.rgb)
        self.assertEqual(yellow.new_brightness_color(120).rgb, yellow.rgb)

    def test_new_invert_color(self):
        yellow = Color((255, 255, 0))
        orange = Color((255, 165, 0))
        blue = Color((0, 0, 255))
        royalblue = Color((65,105, 225))
        gray = Color((128, 128, 128))

        self.assertEqual(yellow.new_invert_color(0).rgb, yellow.rgb)
        self.assertEqual(orange.new_invert_color(0).rgb, orange.rgb)
        self.assertEqual(blue.new_invert_color(0).rgb, blue.rgb)
        self.assertEqual(royalblue.new_invert_color(0).rgb, royalblue.rgb)
        self.assertEqual(gray.new_invert_color(0).rgb, gray.rgb)

        self.assertEqual(yellow.new_invert_color().rgb, blue.rgb)
        self.assertEqual(yellow.new_invert_color(100).rgb, blue.rgb)
        self.assertEqual(blue.new_invert_color(100).rgb, yellow.rgb)

        self.assertEqual(orange.new_invert_color(100).rgb, (0, 90, 255))
        self.assertEqual(royalblue.new_invert_color(100).rgb, (190, 150, 30))

        self.assertEqual(yellow.new_invert_color(50).rgb, gray.rgb)
        self.assertEqual(orange.new_invert_color(50).rgb, gray.rgb)
        self.assertEqual(blue.new_invert_color(50).rgb, gray.rgb)
        self.assertEqual(royalblue.new_invert_color(50).rgb, gray.rgb)
        self.assertEqual(gray.new_invert_color(50).rgb, gray.rgb)

    def test_new_hue_rotate_color(self):
        yellow = Color((255, 255, 0))
        orange = Color((255, 165, 0))
        blue = Color((0, 0, 255))

        self.assertEqual(yellow.new_hue_rotate_color(0).rgb, yellow.rgb)
        self.assertEqual(orange.new_hue_rotate_color(0).rgb, orange.rgb)
        self.assertEqual(blue.new_hue_rotate_color(0).rgb, blue.rgb)

        self.assertEqual(yellow.new_hue_rotate_color(360).rgb, yellow.rgb)
        self.assertEqual(orange.new_hue_rotate_color(360).rgb, orange.rgb)
        self.assertEqual(blue.new_hue_rotate_color(360).rgb, blue.rgb)

        self.assertEqual(yellow.new_hue_rotate_color(180).rgb, (218, 218, 255))
        self.assertEqual(orange.new_hue_rotate_color(180).rgb, (90, 180, 255))
        self.assertEqual(blue.new_hue_rotate_color(180).rgb, (37, 37, 0))

        self.assertEqual(yellow.new_hue_rotate_color(90).rgb, (0, 255, 218))
        self.assertEqual(orange.new_hue_rotate_color(90).rgb, (0, 232, 90))
        self.assertEqual(blue.new_hue_rotate_color(90).rgb, (255, 0, 37))

    def test_new_saturate_color(self):
        red = Color((255, 0, 0))
        orange = Color((255, 165, 0))
        yellow = Color((255, 255, 0))
        blue = Color((0, 0, 255))

        self.assertEqual(orange.new_saturate_color(100).rgb, orange.rgb)
        self.assertEqual(yellow.new_saturate_color(100).rgb, yellow.rgb)
        self.assertEqual(blue.new_saturate_color(100).rgb, blue.rgb)

        self.assertEqual(orange.new_saturate_color(0).rgb, (172, 172, 172))
        self.assertEqual(yellow.new_saturate_color(0).rgb, (237, 237, 237))
        self.assertEqual(blue.new_saturate_color(0).rgb, (18, 18, 18))

        self.assertEqual(orange.new_saturate_color(2357).rgb, red.rgb)
        self.assertEqual(orange.new_saturate_color(3000).rgb, red.rgb)

    def test_WHITE(self):
        self.assertTrue(isinstance(Color.WHITE, Color))
        self.assertEqual(Color.WHITE.name, 'white')
        self.assertEqual(Color.WHITE.hex, '#ffffff')

    def test_GRAY(self):
        self.assertTrue(isinstance(Color.GRAY, Color))
        self.assertEqual(Color.GRAY.name, 'gray')
        self.assertEqual(Color.GRAY.hex, '#808080')

    def test_BLACK(self):
        self.assertTrue(isinstance(Color.BLACK, Color))
        self.assertEqual(Color.BLACK.name, 'black')
        self.assertEqual(Color.BLACK.hex, '#000000')
