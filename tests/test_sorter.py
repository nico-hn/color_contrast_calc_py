import unittest
import operator
from color_contrast_calc.color import Color
from color_contrast_calc import sorter
from color_contrast_calc import utils

class TestSorter(unittest.TestCase):
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

    def test_compile_hex_sort_key_function(self):
        hsl_hex = utils.hsl_to_hex((20, 80, 50))
        rgb_hex = utils.rgb_to_hex((10, 165, 70))

        key_func = sorter.compile_hex_sort_key_function('hsl')
        for k, h in zip(key_func(hsl_hex), (20, 80, 50)):
            self.assertAlmostEqual(k, h, 0)

        key_func = sorter.compile_hex_sort_key_function('HSL')
        for k, h in zip(key_func(hsl_hex), (-20, -80, -50)):
            self.assertAlmostEqual(k, h, 0)

        key_func = sorter.compile_hex_sort_key_function('lHs')
        for k, h in zip(key_func(hsl_hex), (50, -20, 80)):
            self.assertAlmostEqual(k, h, 0)

        key_func = sorter.compile_hex_sort_key_function('rgb')
        for k, h in zip(key_func(rgb_hex), (10, 165, 70)):
            self.assertEqual(k, h, 0)

        key_func = sorter.compile_hex_sort_key_function('bRG')
        for k, h in zip(key_func(rgb_hex), (70, -10, -165)):
            self.assertEqual(k, h, 0)

    def test_compile_color_sort_key_function(self):
        hsl = Color.new_from_hsl((20, 80, 50))
        rgb = Color((10, 165, 70))

        key_func = sorter.compile_color_sort_key_function('hsl')
        for k, h in zip(key_func(hsl), (20, 80, 50)):
            self.assertAlmostEqual(k, h, 0)

        key_func = sorter.compile_color_sort_key_function('HSL')
        for k, h in zip(key_func(hsl), (-20, -80, -50)):
            self.assertAlmostEqual(k, h, 0)

        key_func = sorter.compile_color_sort_key_function('lHs')
        for k, h in zip(key_func(hsl), (50, -20, 80)):
            self.assertAlmostEqual(k, h, 0)

        key_func = sorter.compile_color_sort_key_function('rgb')
        for k, h in zip(key_func(rgb), (10, 165, 70)):
            self.assertEqual(k, h, 0)

        key_func = sorter.compile_color_sort_key_function('bRG')
        for k, h in zip(key_func(rgb), (70, -10, -165)):
            self.assertEqual(k, h, 0)

    def test_compose_key_function(self):
        hsl = Color.new_from_hsl((20, 80, 50))
        rgb = Color((10, 165, 70))
        hsl_func = sorter.compile_color_sort_key_function('lHs')
        rgb_func = sorter.compile_color_sort_key_function('bRG')

        key_func = sorter.compose_key_function(hsl_func)
        for k, h in zip(key_func(hsl), (50, -20, 80)):
            self.assertAlmostEqual(k, h, 0)

        key_func = sorter.compose_key_function(hsl_func, operator.itemgetter(0))
        for k, h in zip(key_func([hsl]), (50, -20, 80)):
            self.assertAlmostEqual(k, h, 0)

        key_func = sorter.compose_key_function(rgb_func)
        for k, h in zip(key_func(rgb), (70, -10, -165)):
            self.assertAlmostEqual(k, h, 0)

        key_func = sorter.compose_key_function(rgb_func, operator.itemgetter(0))
        for k, h in zip(key_func([rgb]), (70, -10, -165)):
            self.assertAlmostEqual(k, h, 0)