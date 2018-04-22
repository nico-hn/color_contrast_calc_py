import unittest
from color_contrast_calc.threshold_finders import brightness
from color_contrast_calc.color import Color

class TestBrightness(unittest.TestCase):
    def setup(self):
        pass

    def test_find(self):
        black = Color.from_name('black')
        white = Color.from_name('white')
        brown = Color.from_name('brown')
        orange = Color.from_name('orange')
        mintcream = Color.from_name('mintcream')
        yellow = Color.from_name('yellow')
        springgreen = Color.from_name('springgreen')
        green = Color.from_name('green')
        darkgreen = Color.from_name('darkgreen')
        blue = Color.from_name('blue')
        azure = Color.from_name('azure')
        blueviolet = Color.from_name('blueviolet')
        fuchsia = Color.from_name('fuchsia')

        fixed_color = orange
        new_rgb = brightness.find(fixed_color.rgb, fixed_color.rgb)
        new_color = Color(new_rgb)
        new_contrast_ratio = fixed_color.contrast_ratio_against(new_color)
        self.assertLess(fixed_color.contrast_ratio_against(fixed_color), 4.5)
        self.assertGreater(new_contrast_ratio, 4.5)
        self.assertAlmostEqual(new_contrast_ratio, 4.5, 1)
        self.assertEqual(new_color.hex, '#674200')

        fixed_color = orange
        new_rgb = brightness.find(fixed_color.rgb, blueviolet.rgb)
        new_color = Color(new_rgb)
        new_contrast_ratio = fixed_color.contrast_ratio_against(new_color)
        self.assertGreater(new_contrast_ratio, 4.5)
        self.assertAlmostEqual(new_contrast_ratio, 4.5, 1)
        self.assertEqual(new_color.hex, '#6720a9')

        fixed_color = blue
        new_rgb = brightness.find(fixed_color.rgb, orange.rgb)
        new_color = Color(new_rgb)
        new_contrast_ratio = fixed_color.contrast_ratio_against(new_color)
        self.assertGreater(new_contrast_ratio, 4.5)
        self.assertAlmostEqual(new_contrast_ratio, 4.5, 1)
        self.assertEqual(new_color.hex, '#ffaa00')

        fixed_color = blueviolet
        new_rgb = brightness.find(fixed_color.rgb, orange.rgb)
        new_color = Color(new_rgb)
        new_contrast_ratio = fixed_color.contrast_ratio_against(new_color)
        self.assertGreater(new_contrast_ratio, 4.5)
        self.assertAlmostEqual(new_contrast_ratio, 4.5, 1)
        self.assertEqual(new_color.hex, '#ffe000')

        fixed_color = brown
        new_rgb = brightness.find(fixed_color.rgb, fixed_color.rgb)
        new_color = Color(new_rgb)
        new_contrast_ratio = fixed_color.contrast_ratio_against(new_color)
        self.assertEqual(brown.hex, '#a52a2a')
        self.assertGreater(new_contrast_ratio, 4.5)
        self.assertAlmostEqual(new_contrast_ratio, 4.5, 1)
        self.assertEqual(new_color.hex, '#ffbebe')

        new_rgb = brightness.find(white.rgb, darkgreen.rgb)
        new_color = Color(new_rgb)
        new_contrast_ratio = white.contrast_ratio_against(new_color)
        self.assertGreater(new_contrast_ratio, 4.5)
        self.assertAlmostEqual(new_contrast_ratio, 4.5, 1)

        new_rgb = brightness.find(white.rgb, darkgreen.rgb, 'AAA')
        new_color = Color(new_rgb)
        new_contrast_ratio = white.contrast_ratio_against(new_color)
        self.assertGreater(new_contrast_ratio, 7)
        self.assertAlmostEqual(new_contrast_ratio, 7, 1)

        new_rgb = brightness.find(green.rgb, blue.rgb)
        new_color = Color(new_rgb)
        self.assertTrue(new_color.is_same_color(black))

        self.assertTrue(mintcream.has_higher_luminance(yellow))

        new_color = mintcream.with_brightness(105)
        self.assertEqual(brightness.calc_upper_ratio_limit(mintcream.rgb), 105)
        self.assertTrue(new_color.is_same_color(white))

        new_rgb = brightness.find(yellow.rgb, mintcream.rgb, 'A')
        new_color = Color(new_rgb)
        self.assertTrue(new_color.is_same_color(white))

        new_rgb = brightness.find(yellow.rgb, mintcream.rgb, 'AA')
        new_color = Color(new_rgb)
        self.assertTrue(new_color.is_same_color(white))

        new_rgb = brightness.find(yellow.rgb, mintcream.rgb, 'AAA')
        self.assertTrue(new_color.is_same_color(white))

    def test_calc_upper_ratio_limit(self):
        color = Color.from_name('black')
        self.assertEqual(brightness.calc_upper_ratio_limit(color.rgb), 100)

        color = color.from_name('orange')
        self.assertEqual(brightness.calc_upper_ratio_limit(color.rgb), 155)

        color = color.from_name('blueviolet')
        self.assertEqual(brightness.calc_upper_ratio_limit(color.rgb), 594)

        color = Color((0, 180, 0))
        self.assertEqual(brightness.calc_upper_ratio_limit(color.rgb), 142)
