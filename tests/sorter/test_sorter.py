import unittest
import operator
from color_contrast_calc.color import Color
from color_contrast_calc.sorter import sorter
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
        pos = sorted(order['funcs'].keys())
        descend = tuple(order['funcs'][i](1) for i in pos)
        self.assertEqual(order['pos'], (0, 1, 2))
        self.assertEqual(descend, (1, 1, 1))

        order = sorter.parse_color_order('HSL')
        pos = sorted(order['funcs'].keys())
        descend = tuple(order['funcs'][i](1) for i in pos)
        self.assertEqual(order['pos'], (0, 1, 2))
        self.assertEqual(descend, (-1, -1, -1))

        order = sorter.parse_color_order('lHs')
        pos = sorted(order['funcs'].keys())
        descend = tuple(order['funcs'][i](1) for i in pos)
        print(order)
        self.assertEqual(order['pos'], (2, 0, 1))
        self.assertEqual(descend, (-1, 1, 1))

        order = sorter.parse_color_order('rgb')
        pos = sorted(order['funcs'].keys())
        descend = tuple(order['funcs'][i](1) for i in pos)
        self.assertEqual(order['pos'], (0, 1, 2))
        self.assertEqual(descend, (1, 1, 1))

        order = sorter.parse_color_order('bRG')
        pos = sorted(order['funcs'].keys())
        descend = tuple(order['funcs'][i](1) for i in pos)
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
        hsl = Color.from_hsl((20, 80, 50))
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
        hsl = Color.from_hsl((20, 80, 50))
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

class TestSorterSortedColor(unittest.TestCase):
    def setUp(self):
        self.color_names = [
            'black',
            'gray',
            'orange',
            'yellow',
            'springgreen',
            'blue'
        ]

        self.color_names2 = [
            'white',
            'red',
            'yellow',
            'lime',
            'blue'
        ]

        self.prepare_colors()

    def prepare_colors(self):
        self.colors = [Color.from_name(c) for c in self.color_names]
        self.colors2 = [Color.from_name(c) for c in self.color_names2]
        self.key = None

    def __assert_sorted_result(self, order, before, after):
        self.assertEqual(sorter.sorted(before, order, self.key), after)

    def test_rgb(self):
        black, gray, orange, yellow, springgreen, blue = self.colors

        order =  'rgb'
        self.__assert_sorted_result(order,
                                    [black, yellow, orange],
                                    [black, orange, yellow])
        self.__assert_sorted_result(order,
                                    [black, yellow, orange, springgreen],
                                    [black, springgreen, orange, yellow])
        self.__assert_sorted_result(order,
                                    [yellow, black, orange],
                                    [black, orange, yellow])
        self.__assert_sorted_result(order,
                                    [yellow, black, orange, gray],
                                    [black, gray, orange, yellow])
        self.__assert_sorted_result(order,
                                    [yellow, black, orange, blue],
                                    [black, blue, orange, yellow])

        order = 'grb'
        self.__assert_sorted_result(order,
                                    [black, yellow, orange],
                                    [black, orange, yellow])
        self.__assert_sorted_result(order,
                                    [black, yellow, orange, springgreen],
                                    [black, orange, springgreen, yellow])
        self.__assert_sorted_result(order,
                                    [yellow, black, orange],
                                    [black, orange, yellow])
        self.__assert_sorted_result(order,
                                    [yellow, black, orange, gray],
                                    [black, gray, orange, yellow])
        self.__assert_sorted_result(order,
                                    [yellow, black, orange, blue],
                                    [black, blue, orange, yellow])

        order = 'brg'
        self.__assert_sorted_result(order,
                                    [black, yellow, orange],
                                    [black, orange, yellow])
        self.__assert_sorted_result(order,
                                    [black, yellow, orange, springgreen],
                                    [black, orange, yellow, springgreen])
        self.__assert_sorted_result(order,
                                    [yellow, black, orange],
                                    [black, orange, yellow])
        self.__assert_sorted_result(order,
                                    [yellow, black, orange, gray],
                                    [black, orange, yellow, gray])
        self.__assert_sorted_result(order,
                                    [yellow, black, orange, blue],
                                    [black, orange, yellow, blue])

        order = 'Rgb'
        self.__assert_sorted_result(order,
                                    [black, yellow, orange],
                                    [orange, yellow, black])
        self.__assert_sorted_result(order,
                                    [black, yellow, orange, springgreen],
                                    [orange, yellow, black, springgreen])
        self.__assert_sorted_result(order,
                                    [yellow, black, orange],
                                    [orange, yellow, black])
        self.__assert_sorted_result(order,
                                    [yellow, black, orange, gray],
                                    [orange, yellow, gray, black])
        self.__assert_sorted_result(order,
                                    [yellow, black, orange, blue],
                                    [orange, yellow, black, blue])

    def test_hsl(self):
        white, red, yellow, lime, blue = self.colors2

        order = 'hLS'
        self.__assert_sorted_result(order,
                                    [blue, yellow, white, red, lime],
                                    [white, red, yellow, lime, blue])

class TestSorterSortedRGB(TestSorterSortedColor):
    def prepare_colors(self):
        self.colors = [Color.from_name(c).rgb for c in self.color_names]
        self.colors2 = [Color.from_name(c).hsl for c in self.color_names2]
        self.key = None

class TestSorterSortedHex(TestSorterSortedColor):
    def prepare_colors(self):
        self.colors = [Color.from_name(c).hex for c in self.color_names]
        self.colors2 = [Color.from_name(c).hex for c in self.color_names2]
        self.key = None

class TestSorterSortedColorInArray(TestSorterSortedColor):
    def prepare_colors(self):
        self.colors = [[Color.from_name(c)] for c in self.color_names]
        self.colors2 = [[Color.from_name(c)] for c in self.color_names2]
        self.key = operator.itemgetter(0)

class TestSorterSortedRGBInArray(TestSorterSortedColor):
    def prepare_colors(self):
        self.colors = [[Color.from_name(c).rgb] for c in self.color_names]
        self.colors2 = [[Color.from_name(c).hsl] for c in self.color_names2]
        self.key = operator.itemgetter(0)

class TestSorterSortedHexInArray(TestSorterSortedColor):
    def prepare_colors(self):
        self.colors = [[Color.from_name(c).hex] for c in self.color_names]
        self.colors2 = [[Color.from_name(c).hex] for c in self.color_names2]
        self.key = operator.itemgetter(0)
