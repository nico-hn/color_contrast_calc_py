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
