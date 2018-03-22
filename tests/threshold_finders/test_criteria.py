import unittest
from color_contrast_calc.threshold_finders.criteria import threshold_criteria
from color_contrast_calc.color import Color

class TestCriteria(unittest.TestCase):
    def setup(self):
        pass

    def test_criteria(self):
        target = 'AA'
        orange = Color.from_name('orange').rgb
        yellow = Color.from_name('yellow').rgb
        darkgreen = Color.from_name('darkgreen').rgb

        direction = threshold_criteria(target, orange, yellow)
        self.assertTrue(direction.increment_condition(4.25))
        self.assertEqual(direction.round(4.25), 4.3)

        direction = threshold_criteria(target, yellow, orange)
        self.assertFalse(direction.increment_condition(4.25))
        self.assertEqual(direction.round(4.25), 4.2)

        direction = threshold_criteria(target, yellow, yellow)
        self.assertFalse(direction.increment_condition(4.25))
        self.assertEqual(direction.round(4.25), 4.2)

        direction = threshold_criteria(target, darkgreen, darkgreen)
        self.assertTrue(direction.increment_condition(4.25))
        self.assertEqual(direction.round(4.25), 4.3)
