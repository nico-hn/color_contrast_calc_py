import unittest
import operator
from color_contrast_calc.color import Color
from color_contrast_calc.sorter import _sorter, key_types

class TestKeyTypes(unittest.TestCase):
    def setUp(self):
        pass

    def test_guess(self):
        color = Color((255, 255, 0))
        rgb = (255, 255, 0)
        hsl = (60, 100, 50)
        hex = '#ffff00'
        colors = [color, rgb, hsl, hex]

        self.assertEqual(key_types.guess(color), key_types.COLOR)
        self.assertEqual(key_types.guess(colors, operator.itemgetter(0)),
                         key_types.COLOR)

        self.assertEqual(key_types.guess(rgb), key_types.COMPONENTS)
        self.assertEqual(key_types.guess(colors, operator.itemgetter(1)),
                         key_types.COMPONENTS)

        self.assertEqual(key_types.guess(hsl), key_types.COMPONENTS)
        self.assertEqual(key_types.guess(colors, operator.itemgetter(2)),
                         key_types.COMPONENTS)

        self.assertEqual(key_types.guess(hex), key_types.HEX)
        self.assertEqual(key_types.guess(colors, operator.itemgetter(3)),
                         key_types.HEX)
