import unittest
from color_contrast_calc.threshold_finders import binary_search_width

class TestThresholdFinder(unittest.TestCase):
    def setup(self):
        pass

    def test_binary_search_width(self):
        ds = []
        for d in binary_search_width(100, 1):
            ds.append(d)

        for d in ds:
            self.assertFalse(isinstance(d, int))

        self.assertEqual(ds, [50, 25, 12.5, 6.25, 3.125, 1.5625])
