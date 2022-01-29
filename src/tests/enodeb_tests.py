import unittest

from src.models.map_time_models import Position2d
from src.sumo.net_file_parse import extract_projection_details_from_net_file
from src.tests.uct_tests import create_eNodeBs
from src.v2x.enodeb import read_eNodeBs_from_config_file, project_and_add_net_offset_for_eNodeBs, assign_boundaries, \
    get_eNodeB_id_by_location


class MyTestCase(unittest.TestCase):
    def test_create_eNodeBs_and_assign_boundaries(self):
        """Not really unit test :)
        """
        sumo_net_file = '/home/chris/Documents/STUDIA/Praca_mgr/Symulacje/v2x-mec/sumo/net_s8/osm.net.xml'
        eNodeB_mec_conf_file = '/home/chris/Documents/STUDIA/Praca_mgr/Symulacje/v2x-mec/bts/bts-mec-conf.json'

        net_offset, conv_bbox, orig_bbox, proj_params = extract_projection_details_from_net_file(sumo_net_file)
        eNodeBs = read_eNodeBs_from_config_file(eNodeB_mec_conf_file)
        project_and_add_net_offset_for_eNodeBs(eNodeBs, net_offset, proj_params)
        assign_boundaries(eNodeBs, conv_bbox)

        self.assertTrue(all(map(lambda enb: len(enb.boundary_points) != 0 or enb.boundary_points is not None, eNodeBs)))

    def test_get_eNodeB_id_by_location(self):
        eNodeBs = create_eNodeBs()

        locations_expected_mec_ids = [
            [Position2d(2.11, 9.99), 5],
            [Position2d(4.01, 2.9999), 2],
            [Position2d(7.01, 3.15), 4],
            [Position2d(0.01, 0.01), 0],
            [Position2d(2.01, 2.01), 1],
        ]

        for location_expected_mec_id in locations_expected_mec_ids:
            actual_id = get_eNodeB_id_by_location(location_expected_mec_id[0], eNodeBs)
            expected_id = location_expected_mec_id[1]
            self.assertEqual(expected_id, actual_id)