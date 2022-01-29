import unittest
from typing import List

from src.models.map_time_models import Position2d, CarInfo, TimeLocation
from src.models.v2x_models import Mec, eNodeB, UctStats
from src.v2x.mec import extract_mecs_with_ranges
from src.v2x.uct import UctCalc


class MyTestCase(unittest.TestCase):
    def test_retrieve_ucts_and_calculate_stats_one_eNodeB_per_mec(self):
        eNodeBs = create_eNodeBs()
        mecs = create_mecs_one_eNodeB_per_mec(eNodeBs)
        car_time_locations = create_car_time_locations()

        uct_calc = UctCalc()
        uct_stats = uct_calc.retrieve_ucts_and_calculate_stats(car_time_locations, eNodeBs, mecs)

        expected_stats = UctStats()
        expected_stats.all_uct_count = 50
        expected_stats.max_uct_freq = 1.75
        expected_stats.min_uct_freq = 4/7
        expected_stats.mecs_uct_stats = [
            {
                'mec_id': 0,
                'included_eNodeBs': [0],
                'uct_freq': 14 / (8 - 0),  # 1.75
                'uct_count': 14
            },
            {
                'mec_id': 1,
                'included_eNodeBs': [1],
                'uct_freq': 14 / (9 - 1),  # 1.75
                'uct_count': 14
            },
            {
                'mec_id': 2,
                'included_eNodeBs': [2],
                'uct_freq': 8 / (11 - 4),  # 8/7
                'uct_count': 8
            },
            {
                'mec_id': 3,
                'included_eNodeBs': [3],
                'uct_freq': 4 / (12 - 5),  # 0.57
                'uct_count': 4
            },
            {
                'mec_id': 4,
                'included_eNodeBs': [4],
                'uct_freq': 4 / 7,    # 0.57
                'uct_count': 4
            },
            {
                'mec_id': 5,
                'included_eNodeBs': [5],
                'uct_freq': 6 / 7,  # 0.86
                'uct_count': 6
            },
        ]

        self.assertEqual(expected_stats.max_uct_freq, uct_stats.max_uct_freq)
        self.assertEqual(expected_stats.min_uct_freq, uct_stats.min_uct_freq)
        self.assertEqual(expected_stats.all_uct_count, uct_stats.all_uct_count)

        for mec_stats in uct_stats.mecs_uct_stats:
            expected_mec = next(filter(lambda mec: mec['mec_id'] == mec_stats['mec_id'], expected_stats.mecs_uct_stats))
            self.assertEqual(expected_mec['uct_freq'], mec_stats['uct_freq'])
            self.assertEqual(expected_mec['uct_count'], mec_stats['uct_count'])
            self.assertEqual(expected_mec['included_eNodeBs'][0], mec_stats['included_eNodeBs'][0])


def create_mecs_one_eNodeB_per_mec(eNodeBs: List[eNodeB]) -> List[Mec]:
    for enb in eNodeBs:
        enb.assigned_mec_id = enb.Id

    return extract_mecs_with_ranges(eNodeBs)


def create_car_time_locations() -> List[List]:
    """trip = [time, car_id, x, y]"""
    car_time_locations = [
        # 1 trip
        [0, '0', 1, 1],  # enb0
        [1, '0', 1, 2],  # enb0 -> enb1
        [2, '0', 3, 2.5],  # enb1 -> enb5
        [3, '0', 3, 5],  # enb5
        [4, '0', 3, 7],  # enb5 -> enb4
        [5, '0', 7, 7],  # enb4
        [6, '0', 8, 8],  # enb4

        [0, '1', 1, 1],
        [1, '1', 1, 2],
        [2, '1', 3, 2.5],
        [3, '1', 3, 5],
        [4, '1', 3, 7],
        [5, '1', 7, 7],
        [6, '1', 8, 8],

        [0, '2', 1, 1],
        [1, '2', 1, 2],
        [2, '2', 3, 2.5],
        [3, '2', 3, 5],
        [4, '2', 3, 7],
        [5, '2', 7, 7],
        [6, '2', 8, 8],

        # 1 trip
        [7, '3', 1, 1],  # enb0
        [8, '3', 1, 2],  # enb0 -> enb1
        [9, '3', 3, 2.5],  # enb1 -> enb5
        [10, '3', 3, 5],  # enb5
        [11, '3', 3, 7],  # enb5 -> enb4
        [12, '3', 7, 7],  # enb4
        [13, '3', 8, 8],  # enb4

        [7, '4', 1, 1],
        [8, '4', 1, 2],
        [9, '4', 3, 2.5],
        [10, '4', 3, 5],
        [11, '4', 3, 7],
        [12, '4', 7, 7],
        [13, '4', 8, 8],

        [7, '5', 1, 1],
        [8, '5', 1, 2],
        [9, '5', 3, 2.5],
        [10, '5', 3, 5],
        [11, '5', 3, 7],
        [12, '5', 7, 7],
        [13, '5', 8, 8],

        # 2. trip
        [0, '6', 1, 1],    # enb0 -> enb1
        [1, '6', 3, 2.5],    # enb1 -> enb2
        [2, '6', 5, 2],    # enb2
        [3, '6', 5, 2.5],  # enb2 -> enb4
        [4, '6', 8, 4],    # enb4 -> enb3
        [5, '6', 8, 2],  # enb3
        [6, '6', 9, 2],  # enb3

        [0, '7', 1, 1],
        [1, '7', 3, 2.5],
        [2, '7', 5, 2],
        [3, '7', 5, 2.5],
        [4, '7', 8, 4],
        [5, '7', 8, 2],
        [6, '7', 9, 2],

        # 2. trip
        [7, '8', 1, 1],  # enb0 -> enb1
        [8, '8', 3, 2.5],  # enb1 -> enb2
        [9, '8', 5, 2],  # enb2
        [10, '8', 5, 2.5],  # enb2 -> enb4
        [11, '8', 8, 4],  # enb4 -> enb3
        [12, '8', 8, 2],
        [13, '8', 9, 2],

        [7, '9', 1, 1],
        [8, '9', 3, 2.5],
        [9, '9', 5, 2],
        [10, '9', 5, 2.5],
        [11, '9', 8, 4],
        [12, '9', 8, 2],
        [13, '9', 9, 2],

        # 3. trip
        [0, '10', 1, 1],    # enb0
        [1, '10', 2, 0.5],  # enb0 -> enb1
        [2, '10', 3, 1.5],    # enb1 -> enb2
        [3, '10', 5, 1],    # enb2 -> enb3
        [4, '10', 8, 1],    # enb3
        [5, '10', 9, 2],    # enb3 -> enb4
        [6, '10', 9, 5],    # enb4

        [0, '11', 1, 1],
        [1, '11', 2, 0.5],
        [2, '11', 3, 1.5],
        [3, '11', 5, 1],
        [4, '11', 8, 1],
        [5, '11', 9, 2],
        [6, '11', 9, 5],

        # 3. trip
        [7, '12', 1, 1],  # enb0
        [8, '12', 2, 0.5],  # enb0 -> enb1
        [9, '12', 3, 1.5],  # enb1 -> enb2
        [10, '12', 5, 1],  # enb2 -> enb3
        [11, '12', 8, 1],  # enb3
        [12, '12', 9, 2],  # enb3 -> enb4
        [13, '12', 9, 5],  # enb4

        [7, '13', 1, 1],
        [8, '13', 2, 0.5],
        [9, '13', 3, 1.5],
        [10, '13', 5, 1],
        [11, '13', 8, 1],
        [12, '13', 9, 2],
        [13, '13', 9, 5],
    ]

    return sorted(car_time_locations, key=lambda x: x[0])


def create_eNodeBs() -> List[eNodeB]:
    enb0 = eNodeB(0, 1.5, 1.5)
    enb0.boundary_points = [
        (0, 0),
        (4, 0),
        (0, 3)
    ]

    enb1 = eNodeB(1, 2.5, 2.5)
    enb1.boundary_points = [
        (4, 0),
        (4, 3),
        (0, 3)
    ]

    enb2 = eNodeB(2, 6, 2)
    enb2.boundary_points = [
        (4, 0),
        (7, 0),
        (7, 3),
        (4, 3)
    ]

    enb3 = eNodeB(3, 8, 2)
    enb3.boundary_points = [
        (7, 0),
        (10, 0),
        (10, 3),
        (7, 3)
    ]

    enb4 = eNodeB(4, 7, 7)
    enb4.boundary_points = [
        (4, 3),
        (10, 3),
        (10, 10),
        (4, 10)
    ]

    enb5 = eNodeB(5, 2, 7)
    enb5.boundary_points = [
        (0, 3),
        (4, 3),
        (4, 10),
        (0, 10)
    ]

    return [enb0, enb1, enb2, enb3, enb4, enb5]


if __name__ == '__main__':
    unittest.main()
