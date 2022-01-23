import unittest

from src.sumo.net_file_parse import extract_projection_details_from_net_file
from src.v2x.enodeb import read_eNodeBs_from_config_file, project_and_add_net_offset_for_eNodeBs, assign_boundaries


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
