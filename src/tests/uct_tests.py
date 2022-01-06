import unittest
from typing import List

from src.models.map_time_models import Position2d, CarInfo, TimeLocation
from src.models.v2x_models import Mec
from src.v2x.uct import assign_ucts_to_mecs, calculate_uct_stats, get_uct_frequency_for_mec


class MyTestCase(unittest.TestCase):
    def test_assign_ucts(self):

        mecs = create_mecs()
        cars = create_cars()

        assign_ucts_to_mecs(cars, mecs)

        expected_mecs_utc_counts = [3, 3, 2]
        for index, mec in enumerate(mecs):
            self.assertEqual(len(mec.ucts), expected_mecs_utc_counts[index])

    def test_get_uct_frequency_for_mec(self):
        cars0 = []
        cars2 = create_cars()

        expected_frequencies = [0, 3/4.0]

        for index, cars in enumerate([cars0, cars2]):
            mecs = create_mecs()
            assign_ucts_to_mecs(cars, mecs)

            frequency = get_uct_frequency_for_mec(mecs[0])
            self.assertEqual(frequency, expected_frequencies[index])

    def test_calculate_ucts_stats(self):
        mecs = create_mecs()
        cars = create_cars()

        assign_ucts_to_mecs(cars, mecs)
        global_uct_stats = calculate_uct_stats(mecs)

        expected_uct_count = 8
        expected_max_freq = 2/2
        expected_min_freq = 3/4

        self.assertEqual(expected_max_freq, global_uct_stats.max_uct_freq)
        self.assertEqual(expected_min_freq, global_uct_stats.min_uct_freq)
        self.assertEqual(expected_uct_count, global_uct_stats.all_uct_count)


def create_mecs() -> List[Mec]:
    mec1 = Mec(1)
    mec1.boundary_points.extend([
        Position2d(0, 0),
        Position2d(5, 0),
        Position2d(5, 5),
        Position2d(0, 5),
    ])

    mec2 = Mec(2)
    mec2.boundary_points.extend([
        Position2d(0, 5),
        Position2d(5, 5),
        Position2d(10, 5),
        Position2d(0, 10),
    ])

    mec3 = Mec(3)
    mec3.boundary_points.extend([
        Position2d(5, 0),
        Position2d(10, 0),
        Position2d(10, 10),
        Position2d(5, 10),
    ])

    return [mec1, mec2, mec3]


def create_cars() -> List[CarInfo]:
    car1 = CarInfo('c1')
    car1.time_locations.extend([
        TimeLocation(0.0, 2, 2),  # mec1 -> mec2
        TimeLocation(1.0, 2, 7),  # mec2 -> mec3
        TimeLocation(2.0, 9, 7),  # mec3
        TimeLocation(3.0, 9, 2),  # mec3 -> mec1
        TimeLocation(4.0, 2, 2),  # mec1 -> mec2
        TimeLocation(5.0, 2, 8),  # mec2 -> mec3
        TimeLocation(6.0, 9, 8)   # mec3
    ])

    car2 = CarInfo('c2')
    car2.time_locations.extend([
        TimeLocation(0.0, 3, 3),  # mec1
        TimeLocation(1.0, 3, 6),  # mec1 -> mec2
        TimeLocation(2.0, 3, 7),  # mec2
        TimeLocation(3.0, 3, 8),  # mec2 -> mec3
        TimeLocation(4.0, 6, 8),  # mec3
        TimeLocation(5.0, 6, 8),  # mec3 -> mec1
        TimeLocation(6.0, 2, 2)   # mec1
    ])

    return [car1, car2]


if __name__ == '__main__':
    unittest.main()
