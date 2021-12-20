import unittest

from src.v2x.enodeb import extract_eNodeBs_and_create_ranges
from src.v2x.mec import extract_mecs_with_ranges


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


if __name__ == '__main__':
    unittest.main()
