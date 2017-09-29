import unittest
from color_contrast_calc import utils

class TestUtils(unittest.TestCase):
    def setup(self):
        pass

    def test_hex_to_rgb(self):
        self.assertEqual(utils.hex_to_rgb('#fff'),
                         [255, 255, 255])
        self.assertEqual(utils.hex_to_rgb('#fa0'),
                         [255, 170, 0])
        self.assertEqual(utils.hex_to_rgb('#000'),
                         [0, 0, 0])
        self.assertEqual(utils.hex_to_rgb('#ffffff'),
                         [255, 255, 255])
        self.assertEqual(utils.hex_to_rgb('#ffa500'),
                         [255, 165, 0])
        self.assertEqual(utils.hex_to_rgb('#000000'),
                         [0, 0, 0])

    def test_rgb_to_hex(self):
        self.assertEqual(utils.rgb_to_hex([255, 255, 255]),
                         '#ffffff')
        self.assertEqual(utils.rgb_to_hex([255, 165, 0]),
                         '#ffa500')
        self.assertEqual(utils.rgb_to_hex([0, 0, 0]),
                         '#000000')
