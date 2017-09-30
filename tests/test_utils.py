import unittest
from color_contrast_calc import utils

class TestUtils(unittest.TestCase):
    def setup(self):
        pass

    def test_hex_to_rgb(self):
        self.assertEqual(utils.hex_to_rgb('#fff'),
                         (255, 255, 255))
        self.assertEqual(utils.hex_to_rgb('#fa0'),
                         (255, 170, 0))
        self.assertEqual(utils.hex_to_rgb('#000'),
                         (0, 0, 0))
        self.assertEqual(utils.hex_to_rgb('#ffffff'),
                         (255, 255, 255))
        self.assertEqual(utils.hex_to_rgb('#ffa500'),
                         (255, 165, 0))
        self.assertEqual(utils.hex_to_rgb('#000000'),
                         (0, 0, 0))

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
        self.assertEqual(utils.hsl_to_rgb((0, 100, 50)),
                         (255, 0, 0))
        self.assertEqual(utils.hsl_to_rgb((30, 100, 50)),
                         (255, 128, 0))
        self.assertEqual(utils.hsl_to_rgb((60, 100, 50)),
                         (255, 255, 0))
        self.assertEqual(utils.hsl_to_rgb((120, 100, 50)),
                         (0, 255, 0))
        self.assertEqual(utils.hsl_to_rgb((240, 100, 50)),
                         (0, 0, 255))

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

    def test_rgb_to_hsl(self):
        hsl = utils.rgb_to_hsl((255, 0, 0))
        expected = (0, 100, 50)
        self.assertEqual(hsl, expected)

        hsl = utils.rgb_to_hsl((255, 255, 0))
        expected = (60, 100, 50)
        self.assertEqual(hsl, expected)

        hsl = utils.rgb_to_hsl((0, 255, 0))
        expected = (120, 100, 50)
        self.assertEqual(hsl, expected)

        hsl = utils.rgb_to_hsl((0, 128, 0))
        expected = (120, 100, 25)
        for i, c in enumerate(expected):
            self.assertAlmostEqual(hsl[i], c, 0)

        hsl = utils.rgb_to_hsl((0, 255, 255))
        expected = (180, 100, 50)
        self.assertEqual(hsl, expected)

        hsl = utils.rgb_to_hsl((0, 128, 128))
        expected = (180, 100, 25)
        for i, c in enumerate(expected):
            self.assertAlmostEqual(hsl[i], c, 0)

        hsl = utils.rgb_to_hsl((0, 0, 255))
        expected = (240, 100, 50)
        self.assertEqual(hsl, expected)

        hsl = utils.rgb_to_hsl((0, 0, 0))
        expected = (0, 0, 0)
        self.assertEqual(hsl, expected)

        hsl = utils.rgb_to_hsl((255, 255, 255))
        expected = (0, 0, 100)
        self.assertEqual(hsl, expected)

    def test_hex_to_hsl(self):
        hsl = utils.hex_to_hsl('#ff0000')
        expected = (0, 100, 50)
        self.assertEqual(hsl, expected)

        hex_colors = ['#ffffff', '#808080', '#d2691e', '#cd5c5c', '#adff2f']
        for hex in hex_colors:
            hsl = utils.hex_to_hsl(hex)
            self.assertEqual(utils.hsl_to_hex(hsl), hex)

    def test_is_valid_rgb(self):
        self.assertEqual(utils.is_valid_rgb((255, 165, 0)), True)
        self.assertEqual(utils.is_valid_rgb((256, 165, 0)), False)
        self.assertEqual(utils.is_valid_rgb((165, 256, 0)), False)
        self.assertEqual(utils.is_valid_rgb((255, 165, -1)), False)
        self.assertEqual(utils.is_valid_rgb((255, 165)), False)
        self.assertEqual(utils.is_valid_rgb((255, 165.5, 0)), False)
