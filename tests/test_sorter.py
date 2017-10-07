import unittest
from color_contrast_calc.color import Color
from color_contrast_calc import sorter

class TestLightness(unittest.TestCase):
    def setup(self):
        pass

    def test_is_hsl_order(self):
        self.assertTrue(sorter.is_hsl_order('hsl'))
        self.assertTrue(sorter.is_hsl_order('HSL'))
        self.assertTrue(sorter.is_hsl_order('lHs'))
        self.assertFalse(sorter.is_hsl_order('rgb'))
        self.assertFalse(sorter.is_hsl_order('bRg'))

    def test_color_component_pos(self):
        rgb = 'rgb'
        hsl = 'hsl'

        pos = sorter.color_component_pos('hsl', hsl)
        self.assertEqual(pos, (0, 1, 2))

        pos = sorter.color_component_pos('hLs', hsl)
        self.assertEqual(pos, (0, 2, 1))

        pos = sorter.color_component_pos('rgb', rgb)
        self.assertEqual(pos, (0, 1, 2))

        pos = sorter.color_component_pos('bgr', rgb)
        self.assertEqual(pos, (2, 1, 0))
