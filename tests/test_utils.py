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

    def test_normalize_hex(self):
        self.assertEqual(utils.normalize_hex('#ffa500'),
                         '#ffa500')
        self.assertEqual(utils.normalize_hex('#FFA500'),
                         '#ffa500')
        self.assertEqual(utils.normalize_hex('#fa0'),
                         '#ffaa00')
        self.assertEqual(utils.normalize_hex('ffa500'),
                         '#ffa500')
        self.assertEqual(utils.normalize_hex('FFA500'),
                         '#ffa500')
        self.assertEqual(utils.normalize_hex('fa0'),
                         '#ffaa00')

        self.assertEqual(utils.normalize_hex('#ffa500', False),
                         'ffa500')
        self.assertEqual(utils.normalize_hex('#FFA500', False),
                         'ffa500')
        self.assertEqual(utils.normalize_hex('#fa0', False),
                         'ffaa00')
        self.assertEqual(utils.normalize_hex('ffa500', False),
                         'ffa500')
        self.assertEqual(utils.normalize_hex('FFA500', False),
                         'ffa500')
        self.assertEqual(utils.normalize_hex('fa0', False),
                         'ffaa00')

    def test_hsl_to_rgb(self):
        self.assertEqual(utils.hsl_to_rgb([0, 100, 50]),
                         [255, 0, 0])
        self.assertEqual(utils.hsl_to_rgb([30, 100, 50]),
                         [255, 128, 0])
        self.assertEqual(utils.hsl_to_rgb([60, 100, 50]),
                         [255, 255, 0])
        self.assertEqual(utils.hsl_to_rgb([120, 100, 50]),
                         [0, 255, 0])
        self.assertEqual(utils.hsl_to_rgb([240, 100, 50]),
                         [0, 0, 255])

    def test_hsl_to_hex(self):
        self.assertEqual(utils.hsl_to_hex([0, 100, 50]),
                         '#ff0000')
        self.assertEqual(utils.hsl_to_hex([30, 100, 50]),
                         '#ff8000')
        self.assertEqual(utils.hsl_to_hex([60, 100, 50]),
                         '#ffff00')
        self.assertEqual(utils.hsl_to_hex([120, 100, 50]),
                         '#00ff00')
        self.assertEqual(utils.hsl_to_hex([240, 100, 50]),
                         '#0000ff')
        self.assertEqual(utils.hsl_to_hex([83.653, 100, 59.215]),
                         '#adff2f')
        self.assertEqual(utils.hsl_to_hex([0, 53, 58.2352]),
                         '#cd5c5c')
