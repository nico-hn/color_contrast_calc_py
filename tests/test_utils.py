import unittest
from color_contrast_calc import utils

class TestUtils(unittest.TestCase):
    def setup(self):
        pass

    def test_rgb_to_hex(self):
        self.assertEqual(utils.rgb_to_hex([255, 255, 255]),
                         '#ffffff')
        self.assertEqual(utils.rgb_to_hex([255, 165, 0]),
                         '#ffa500')
        self.assertEqual(utils.rgb_to_hex([0, 0, 0]),
                         '#000000')
