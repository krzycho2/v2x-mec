import unittest

from src.helpers.map_helpers import find_equidistant_y
from src.models.map_time_models import Position2d


class MapHelpersTests(unittest.TestCase):
    def test_find_equidistant_y1(self):
        x = -4
        p1 = Position2d(0, 3)
        p2 = Position2d(0, -3)
        
        expected_y = 0
        
        y = find_equidistant_y(x, p1, p2)
        self.assertAlmostEqual(y, expected_y)

    def test_find_equidistant_y2(self):
        x = 4
        p1 = Position2d(0, 3)
        p2 = Position2d(0, -3)
        
        expected_y = 0
        
        y = find_equidistant_y(x, p1, p2)
        self.assertAlmostEqual(y, expected_y)


if __name__ == '__main__':
    unittest.main()