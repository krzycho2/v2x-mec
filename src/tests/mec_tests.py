import unittest

from src.models.map_time_models import Position2d
from src.models.v2x_models import Mec
from src.v2x.enodeb import extract_eNodeBs_and_create_ranges
from src.v2x.mec import extract_mecs_with_ranges, get_mec_by_location


class MecTests(unittest.TestCase):

    def test_extract_mecs_with_ranges(self):
        eNodeB_mec_config = '/home/chris/Documents/STUDIA/Praca_mgr/Symulacje/v2x-mec/bts/bts-mec-conf.json'
        net_file = '/home/chris/Documents/STUDIA/Praca_mgr/Symulacje/v2x-mec/sumo/net_s8/osm.net.xml'

        eNodeBs = extract_eNodeBs_and_create_ranges(net_file, eNodeB_mec_config)
        mecs = extract_mecs_with_ranges(eNodeBs)

        self.assertEqual(len(mecs), 2)

        enb_len = sum(map(lambda mec: len(mec.included_eNodeBs), mecs))
        self.assertEqual(len(eNodeBs), enb_len)
        self.assertTrue((all(map(lambda mec: mec.boundary_points, mecs))))

    def test_get_mec_by_location_matching_mecs(self):

        mecs = create_2_mecs()

        locations_expected_mecs = [
            {'location': Position2d(5, 5), 'expected_mec_id': 1},
            {'location': Position2d(15, 15), 'expected_mec_id': 2}
        ]

        for location_expected_mec in locations_expected_mecs:
            mec = get_mec_by_location(location_expected_mec['location'], mecs)
            self.assertEqual(mec.Id, location_expected_mec['expected_mec_id'])

    def test_get_mec_by_location_no_matching_mec(self):
        mecs = create_2_mecs()
        location = Position2d(11, 11)
        mec = get_mec_by_location(location, mecs)
        self.assertIsNone(mec)


def create_2_mecs():
    mec1 = Mec(1)
    mec1.boundary_points.extend([Position2d(0, 0),
                                 Position2d(0, 10),
                                 Position2d(10, 10),
                                 Position2d(10, 0)])

    mec2 = Mec(2)
    mec2.boundary_points.extend([Position2d(12, 12),
                                 Position2d(12, 16),
                                 Position2d(16, 16),
                                 Position2d(16, 12)])

    mecs = [mec1, mec2]
    return mecs

if __name__ == '__main__':
    unittest.main()
