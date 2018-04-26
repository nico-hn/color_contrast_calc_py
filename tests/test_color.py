import unittest
from color_contrast_calc.color import Color
from color_contrast_calc.color import NAMED_COLORS
from color_contrast_calc.color import NAME_TO_COLOR
from color_contrast_calc.color import HEX_TO_COLOR
from color_contrast_calc.color import WEB_SAFE_COLORS
from color_contrast_calc.color import hsl_colors

class TestColor(unittest.TestCase):
    def setup(self):
        pass

    def test_from_name(self):
        yellow = Color.from_name('yellow')
        self.assertTrue(isinstance(yellow, Color))
        self.assertEqual(yellow.name, 'yellow')
        self.assertEqual(yellow.hex, '#ffff00')

        yellow = Color.from_name('Yellow')
        self.assertEqual(yellow.name, 'yellow')
        self.assertEqual(yellow.hex, '#ffff00')

        self.assertIsNone(Color.from_name('kiiro'))

    def test_from_hex(self):
        yellow_normalized_hex = '#ffff00'
        yellow_name = 'yellow'
        undefined_color_hex = '#f3f2f1'
        undefined_color_name = 'undefined_color'
        new_yellow_name = 'new_yellow'

        yellow = Color.from_hex(yellow_normalized_hex)
        self.assertTrue(isinstance(yellow, Color))
        self.assertEqual(yellow.name, yellow_name)
        self.assertEqual(yellow.hex, yellow_normalized_hex)

        yellow = Color.from_hex('#FFFF00')
        self.assertTrue(isinstance(yellow, Color))
        self.assertEqual(yellow.name, yellow_name)
        self.assertEqual(yellow.hex, yellow_normalized_hex)

        yellow = Color.from_hex('#ff0')
        self.assertTrue(isinstance(yellow, Color))
        self.assertEqual(yellow.name, yellow_name)
        self.assertEqual(yellow.hex, yellow_normalized_hex)

        undefined_color = Color.from_hex(undefined_color_hex)
        self.assertTrue(isinstance(undefined_color, Color))
        self.assertEqual(undefined_color.name, undefined_color_hex)
        self.assertEqual(undefined_color.hex, undefined_color_hex)

        undefined_color = Color.from_hex(undefined_color_hex, undefined_color_name)
        self.assertEqual(undefined_color.name, undefined_color_name)

        new_yellow = Color.from_hex('#ff0', new_yellow_name)
        self.assertEqual(new_yellow.hex, yellow_normalized_hex)
        self.assertEqual(new_yellow.name, new_yellow_name)

    def test_new_from_hsl(self):
        self.assertEqual(Color.new_from_hsl((60, 100, 50)).hex, '#ffff00')
        self.assertEqual(Color.new_from_hsl((60.0, 100.0, 50.0)).hex, '#ffff00')

        self.assertEqual(Color.new_from_hsl((30, 100, 50)).hex, '#ff8000')
        self.assertEqual(Color.new_from_hsl((30.0, 100.0, 50.0)).hex, '#ff8000')

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

    def test_hsl(self):
        yellow_rgb = (255, 255, 0)
        yellow_hsl = (60, 100, 50)
        yellow = Color(yellow_rgb)

        for i, c in enumerate(yellow_hsl):
            self.assertAlmostEqual(yellow.hsl[i], c)

    def test_rgb_code(self):
        yellow = Color((255, 255, 0))
        yellow_rgb_code = 'rgb(255,255,0)'

        self.assertEqual(yellow.rgb_code, yellow_rgb_code)

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

    def test_with_contrast(self):
        yellow = Color((255, 255, 0))
        orange = Color((255, 165, 0))
        lime = Color((0, 255, 0))
        blue = Color((0, 0, 255))
        white = Color((255, 255, 255))
        black = Color((0, 0, 0))
        neutral_gray = Color((118, 118, 118))
        gray_rgb = (128, 128, 128)

        self.assertEqual(yellow.with_contrast(100).rgb, yellow.rgb)
        self.assertEqual(orange.with_contrast(100).rgb, orange.rgb)
        self.assertEqual(lime.with_contrast(100).rgb, lime.rgb)
        self.assertEqual(blue.with_contrast(100).rgb, blue.rgb)

        self.assertEqual(yellow.with_contrast(0).rgb, gray_rgb)
        self.assertEqual(orange.with_contrast(0).rgb, gray_rgb)
        self.assertEqual(lime.with_contrast(0).rgb, gray_rgb)
        self.assertEqual(blue.with_contrast(0).rgb, gray_rgb)
        self.assertEqual(white.with_contrast(0).rgb, gray_rgb)
        self.assertEqual(black.with_contrast(0).rgb, gray_rgb)
        self.assertEqual(neutral_gray.with_contrast(0).rgb, gray_rgb)

        self.assertEqual(orange.with_contrast(60).rgb, (204, 150, 51))
        self.assertEqual(orange.with_contrast(120).rgb, (255, 173, 0))

    def test_with_brightness(self):
        yellow = Color((255, 255, 0))
        orange = Color((255, 165, 0))
        lime = Color((0, 255, 0))
        blue = Color((0, 0, 255))
        white = Color((255, 255, 255))
        black = Color((0, 0, 0))

        self.assertEqual(yellow.with_brightness(100).rgb, yellow.rgb)
        self.assertEqual(orange.with_brightness(100).rgb, orange.rgb)
        self.assertEqual(lime.with_brightness(100).rgb, lime.rgb)
        self.assertEqual(blue.with_brightness(100).rgb, blue.rgb)

        self.assertEqual(yellow.with_brightness(0).rgb, black.rgb)
        self.assertEqual(orange.with_brightness(0).rgb, black.rgb)
        self.assertEqual(lime.with_brightness(0).rgb, black.rgb)
        self.assertEqual(blue.with_brightness(0).rgb, black.rgb)

        self.assertEqual(white.with_brightness(120).rgb, white.rgb)
        self.assertEqual(yellow.with_brightness(120).rgb, yellow.rgb)

    def test_with_invert(self):
        yellow = Color((255, 255, 0))
        orange = Color((255, 165, 0))
        blue = Color((0, 0, 255))
        royalblue = Color((65,105, 225))
        gray = Color((128, 128, 128))

        self.assertEqual(yellow.with_invert(0).rgb, yellow.rgb)
        self.assertEqual(orange.with_invert(0).rgb, orange.rgb)
        self.assertEqual(blue.with_invert(0).rgb, blue.rgb)
        self.assertEqual(royalblue.with_invert(0).rgb, royalblue.rgb)
        self.assertEqual(gray.with_invert(0).rgb, gray.rgb)

        self.assertEqual(yellow.with_invert().rgb, blue.rgb)
        self.assertEqual(yellow.with_invert(100).rgb, blue.rgb)
        self.assertEqual(blue.with_invert(100).rgb, yellow.rgb)

        self.assertEqual(orange.with_invert(100).rgb, (0, 90, 255))
        self.assertEqual(royalblue.with_invert(100).rgb, (190, 150, 30))

        self.assertEqual(yellow.with_invert(50).rgb, gray.rgb)
        self.assertEqual(orange.with_invert(50).rgb, gray.rgb)
        self.assertEqual(blue.with_invert(50).rgb, gray.rgb)
        self.assertEqual(royalblue.with_invert(50).rgb, gray.rgb)
        self.assertEqual(gray.with_invert(50).rgb, gray.rgb)

    def test_with_hue_rotate(self):
        yellow = Color((255, 255, 0))
        orange = Color((255, 165, 0))
        blue = Color((0, 0, 255))

        self.assertEqual(yellow.with_hue_rotate(0).rgb, yellow.rgb)
        self.assertEqual(orange.with_hue_rotate(0).rgb, orange.rgb)
        self.assertEqual(blue.with_hue_rotate(0).rgb, blue.rgb)

        self.assertEqual(yellow.with_hue_rotate(360).rgb, yellow.rgb)
        self.assertEqual(orange.with_hue_rotate(360).rgb, orange.rgb)
        self.assertEqual(blue.with_hue_rotate(360).rgb, blue.rgb)

        self.assertEqual(yellow.with_hue_rotate(180).rgb, (218, 218, 255))
        self.assertEqual(orange.with_hue_rotate(180).rgb, (90, 180, 255))
        self.assertEqual(blue.with_hue_rotate(180).rgb, (37, 37, 0))

        self.assertEqual(yellow.with_hue_rotate(90).rgb, (0, 255, 218))
        self.assertEqual(orange.with_hue_rotate(90).rgb, (0, 232, 90))
        self.assertEqual(blue.with_hue_rotate(90).rgb, (255, 0, 37))

    def test_with_saturate(self):
        red = Color((255, 0, 0))
        orange = Color((255, 165, 0))
        yellow = Color((255, 255, 0))
        blue = Color((0, 0, 255))

        self.assertEqual(orange.with_saturate(100).rgb, orange.rgb)
        self.assertEqual(yellow.with_saturate(100).rgb, yellow.rgb)
        self.assertEqual(blue.with_saturate(100).rgb, blue.rgb)

        self.assertEqual(orange.with_saturate(0).rgb, (172, 172, 172))
        self.assertEqual(yellow.with_saturate(0).rgb, (237, 237, 237))
        self.assertEqual(blue.with_saturate(0).rgb, (18, 18, 18))

        self.assertEqual(orange.with_saturate(2357).rgb, red.rgb)
        self.assertEqual(orange.with_saturate(3000).rgb, red.rgb)

    def test_with_grayscale(self):
        orange = Color((255, 165, 0))

        self.assertEqual(orange.with_grayscale(0).rgb, orange.rgb)

        self.assertEqual(orange.with_grayscale().rgb, (172, 172, 172))
        self.assertEqual(orange.with_grayscale(100).rgb, (172, 172, 172))

        self.assertEqual(orange.with_grayscale(50).rgb, (214,169, 86))

    def test_find_brightness_threshold(self):
        yellow = Color((255, 255, 0))
        orange = Color((255, 165, 0))

        level = 'A'
        target_ratio = 3.0

        new_color = yellow.find_brightness_threshold(orange, level)
        new_contrast_ratio = yellow.contrast_ratio_against(new_color)
        self.assertTrue(orange.has_higher_luminance(new_color))
        self.assertGreater(new_contrast_ratio, target_ratio)
        self.assertAlmostEqual(new_contrast_ratio, target_ratio, 1)


        new_color = orange.find_brightness_threshold(orange, level)
        new_contrast_ratio = orange.contrast_ratio_against(new_color)
        self.assertTrue(orange.has_higher_luminance(new_color))
        self.assertGreater(new_contrast_ratio, target_ratio)
        self.assertAlmostEqual(new_contrast_ratio, target_ratio, 1)


        level = 'AA'
        target_ratio = 4.5

        new_color = yellow.find_brightness_threshold(orange, level)
        new_contrast_ratio = yellow.contrast_ratio_against(new_color)
        self.assertTrue(orange.has_higher_luminance(new_color))
        self.assertGreater(new_contrast_ratio, target_ratio)
        self.assertAlmostEqual(new_contrast_ratio, target_ratio, 1)


        new_color = orange.find_brightness_threshold(orange, level)
        new_contrast_ratio = orange.contrast_ratio_against(new_color)
        self.assertTrue(orange.has_higher_luminance(new_color))
        self.assertGreater(new_contrast_ratio, target_ratio)
        self.assertAlmostEqual(new_contrast_ratio, target_ratio, 1)


    def test_find_lightness_threshold(self):
        yellow = Color((255, 255, 0))
        orange = Color((255, 165, 0))

        level = 'A'
        target_ratio = 3.0

        new_color = yellow.find_lightness_threshold(orange, level)
        new_contrast_ratio = yellow.contrast_ratio_against(new_color)
        self.assertTrue(orange.has_higher_luminance(new_color))
        self.assertGreater(new_contrast_ratio, target_ratio)
        self.assertAlmostEqual(new_contrast_ratio, target_ratio, 1)


        new_color = orange.find_lightness_threshold(orange, level)
        new_contrast_ratio = orange.contrast_ratio_against(new_color)
        self.assertTrue(orange.has_higher_luminance(new_color))
        self.assertGreater(new_contrast_ratio, target_ratio)
        self.assertAlmostEqual(new_contrast_ratio, target_ratio, 1)


        level = 'AA'
        target_ratio = 4.5

        new_color = yellow.find_lightness_threshold(orange, level)
        new_contrast_ratio = yellow.contrast_ratio_against(new_color)
        self.assertTrue(orange.has_higher_luminance(new_color))
        self.assertGreater(new_contrast_ratio, target_ratio)
        self.assertAlmostEqual(new_contrast_ratio, target_ratio, 1)


        new_color = orange.find_lightness_threshold(orange, level)
        new_contrast_ratio = orange.contrast_ratio_against(new_color)
        self.assertTrue(orange.has_higher_luminance(new_color))
        self.assertGreater(new_contrast_ratio, target_ratio)
        self.assertAlmostEqual(new_contrast_ratio, target_ratio, 1)


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

    def test_NAMED_COLORS(self):
        first_color = NAMED_COLORS[0]
        last_color = NAMED_COLORS[-1]
        self.assertTrue(isinstance(first_color, Color))
        self.assertEqual(first_color.name, 'aliceblue')
        self.assertEqual(first_color.hex, '#f0f8ff')
        self.assertTrue(isinstance(last_color, Color))
        self.assertEqual(last_color.name, 'yellowgreen')
        self.assertEqual(last_color.hex, '#9acd32')
        self.assertEqual(len(NAMED_COLORS), 147)

    def test_NAME_TO_COLOR(self):
        black = 'black'
        white = 'white'
        self.assertEqual(NAME_TO_COLOR[black].name, black)
        self.assertEqual(NAME_TO_COLOR[white].name, white)

    def test_HEX_TO_COLOR(self):
        self.assertEqual(HEX_TO_COLOR['#000000'].name, 'black')
        self.assertEqual(HEX_TO_COLOR['#ffffff'].name, 'white')

    def test_WEB_SAFE_COLORS(self):
        self.assertEqual(len(WEB_SAFE_COLORS), 216)

        first_color = WEB_SAFE_COLORS[0]
        self.assertTrue(isinstance(first_color, Color))
        self.assertEqual(first_color.name, 'black')
        self.assertEqual(first_color.hex, '#000000')

        last_color = WEB_SAFE_COLORS[-1]
        self.assertTrue(isinstance(last_color, Color))
        self.assertEqual(last_color.name, 'white')
        self.assertEqual(last_color.hex, '#ffffff')

        middle_color = WEB_SAFE_COLORS[107]
        self.assertTrue(isinstance(middle_color, Color))
        self.assertEqual(middle_color.hex, '#66ffff')

    def test_hsl_colors(self):
        black = Color.from_name('black')
        white = Color.from_name('white')
        gray = Color.from_name('gray')
        red = Color.from_name('red')
        yellow = Color.from_name('yellow')

        colors = hsl_colors()
        self.assertEqual(len(colors), 361)
        self.assertTrue(colors[0].is_same_color(red))
        self.assertTrue(colors[-1].is_same_color(red))
        self.assertTrue(colors[60].is_same_color(yellow))

        colors = hsl_colors(h_interval = 15)
        self.assertEqual(len(colors), 25)
        self.assertTrue(colors[0].is_same_color(red))
        self.assertTrue(colors[-1].is_same_color(red))
        self.assertTrue(colors[4].is_same_color(yellow))

        colors = hsl_colors(l = 0)
        for c in colors:
            self.assertTrue(c.is_same_color(black))

        colors = hsl_colors(l = 100)
        for c in colors:
            self.assertTrue(c.is_same_color(white))

        colors = hsl_colors(s = 0)
        for c in colors:
            self.assertTrue(c.is_same_color(gray))
