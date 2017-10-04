import unittest
from color_contrast_calc.threshold_finders import lightness
from color_contrast_calc.color import Color

class TestLightness(unittest.TestCase):
    def setup(self):
        pass

    def test_find(self):
        black = Color.from_name('black')
        white = Color.from_name('white')
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

        new_color = lightness.find(fuchsia, azure, 'A')
        new_contrast_ratio = new_color.contrast_ratio_against(fuchsia)
        self.assertTrue(azure.has_higher_luminance(fuchsia))
        self.assertTrue(azure.has_higher_luminance(new_color))
        self.assertEqual(new_color.hex, '#e9ffff')
        self.assertGreater(new_contrast_ratio, 3.0)
        self.assertAlmostEqual(new_contrast_ratio, 3, 1)

        contrast_against_white = darkgreen.contrast_ratio_against(white)
        contrast_against_black = darkgreen.contrast_ratio_against(black)
        new_color = lightness.find(darkgreen, darkgreen, 'A')
        new_contrast_ratio = new_color.contrast_ratio_against(darkgreen)
        self.assertFalse(darkgreen.is_light_color())
        self.assertGreater(contrast_against_white, contrast_against_black)
        self.assertEqual(new_color.hex, '#00c000')
        self.assertTrue(new_color.has_higher_luminance(darkgreen))
        self.assertGreater(new_contrast_ratio, 3.0)
        self.assertAlmostEqual(new_contrast_ratio, 3, 1)

        new_color = lightness.find(white, orange, 'AA')
        new_contrast_ratio = new_color.contrast_ratio_against(white)
        self.assertEqual(new_color.hex, '#a56a00')
        self.assertGreater(new_contrast_ratio, 4.5)
        self.assertAlmostEqual(new_contrast_ratio, 4.5, 1)

        new_color = lightness.find(white, green, 'AA')
        new_contrast_ratio = new_color.contrast_ratio_against(white)
        self.assertEqual(new_color.hex, '#008a00')
        self.assertGreater(new_contrast_ratio, 4.5)
        self.assertAlmostEqual(new_contrast_ratio, 4.5, 1)

        new_color = lightness.find(blueviolet, orange, 'AA')
        new_contrast_ratio = new_color.contrast_ratio_against(blueviolet)
        self.assertEqual(new_color.hex, '#ffdc9a')
        self.assertGreater(new_contrast_ratio, 4.5)
        self.assertAlmostEqual(new_contrast_ratio, 4.5, 1)

        contrast_against_white = springgreen.contrast_ratio_against(white)
        contrast_against_black = springgreen.contrast_ratio_against(black)
        new_color = lightness.find(springgreen, springgreen, 'AA')
        new_contrast_ratio = new_color.contrast_ratio_against(springgreen)
        self.assertTrue(springgreen.is_light_color())
        self.assertLess(contrast_against_white, contrast_against_black)
        self.assertEqual(new_color.hex, '#007239')
        self.assertFalse(new_color.has_higher_luminance(springgreen))
        self.assertGreater(new_contrast_ratio, 4.5)
        self.assertAlmostEqual(new_contrast_ratio, 4.5, 1)

        new_color = lightness.find(orange, yellow)
        self.assertTrue(new_color.is_same_color(white))
        self.assertLess(new_color.contrast_ratio_against(yellow), 4.5)

        new_color = lightness.find(yellow, mintcream)
        self.assertTrue(new_color.is_same_color(white))
        self.assertLess(new_color.contrast_ratio_against(yellow), 4.5)

        new_color = lightness.find(white, orange, 'AAA')
        new_contrast_ratio = new_color.contrast_ratio_against(white)
        self.assertEqual(new_color.hex, '#7b5000')
        self.assertGreater(new_contrast_ratio, 7.0)
        self.assertAlmostEqual(new_contrast_ratio, 7, 1)

        new_color = lightness.find(white, green, 'AAA')
        new_contrast_ratio = new_color.contrast_ratio_against(white)
        self.assertEqual(new_color.hex, '#006800')
        self.assertGreater(new_contrast_ratio, 7.0)
        self.assertAlmostEqual(new_contrast_ratio, 7, 1)

        new_color = lightness.find(green, blue, 'AAA')
        new_contrast_ratio = new_color.contrast_ratio_against(green)
        self.assertTrue(new_color.is_same_color(black))
        self.assertLess(new_contrast_ratio, 7.0)
