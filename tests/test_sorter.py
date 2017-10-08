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

    def test_parse_color_order(self):
        order = sorter.parse_color_order('hsl')
        descend = tuple(order['funcs'][i](1) for i in order['funcs'])
        self.assertEqual(order['pos'], (0, 1, 2))
        self.assertEqual(descend, (1, 1, 1))

        order = sorter.parse_color_order('HSL')
        descend = tuple(order['funcs'][i](1) for i in order['funcs'])
        self.assertEqual(order['pos'], (0, 1, 2))
        self.assertEqual(descend, (-1, -1, -1))

        order = sorter.parse_color_order('lHs')
        descend = tuple(order['funcs'][i](1) for i in order['funcs'])
        self.assertEqual(order['pos'], (2, 0, 1))
        self.assertEqual(descend, (-1, 1, 1))

        order = sorter.parse_color_order('rgb')
        descend = tuple(order['funcs'][i](1) for i in order['funcs'])
        self.assertEqual(order['pos'], (0, 1, 2))
        self.assertEqual(descend, (1, 1, 1))

        order = sorter.parse_color_order('bRG')
        descend = tuple(order['funcs'][i](1) for i in order['funcs'])
        self.assertEqual(order['pos'], (2, 0, 1))
        self.assertEqual(descend, (-1, -1, 1))

    def test_compile_components_sort_key_function(self):
        key_func = sorter.compile_components_sort_key_function('hsl')
        self.assertEqual(key_func((1, 2, 3)), (1, 2, 3))

        key_func = sorter.compile_components_sort_key_function('HSL')
        self.assertEqual(key_func((1, 2, 3)), (-1, -2, -3))

        key_func = sorter.compile_components_sort_key_function('lHs')
        self.assertEqual(key_func((1, 2, 3)), (3, -1, 2))

        key_func = sorter.compile_components_sort_key_function('rgb')
        self.assertEqual(key_func((1, 2, 3)), (1, 2, 3))

        key_func = sorter.compile_components_sort_key_function('bRG')
        self.assertEqual(key_func((1, 2, 3)), (3, -1, -2))
