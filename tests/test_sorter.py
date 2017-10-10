import unittest
import operator
from color_contrast_calc.color import Color
from color_contrast_calc import utils
import color_contrast_calc.sorter as sorter

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
        self.assertEqual(sorter.sorted(before, order, self.key, reverse=True),
                         list(reversed(after)))

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

class TestSorterCompileKeyFunction(unittest.TestCase):
    def setUp(self):
        pass

    def test_key_function_for_color(self):
        rgb = Color((255, 165, 128))
        key_func = sorter.compile_sort_key_function('bRg',
                                                    sorter.key_types.COLOR)
        self.assertEqual(key_func(rgb), (128, -255, 165))

    def test_key_function_for_components(self):
        rgb = (255, 165, 128)
        key_func = sorter.compile_sort_key_function('bRg',
                                                    sorter.key_types.COMPONENTS)
        self.assertEqual(key_func(rgb), (128, -255, 165))

    def test_key_function_for_hex(self):
        rgb = '#ffa580' # same as Color((255, 165, 128)).hex
        key_func = sorter.compile_sort_key_function('bRg',
                                                    sorter.key_types.HEX)
        self.assertEqual(key_func(rgb), (128, -255, 165))
