import unittest


class MyTestCase(unittest.TestCase):
    def test_assign_boundaries_efficient(self):

        eNodeBs = create_eNodeBs()
        bbox = create_bbox()

        self.assertEqual(True, False)  # add assertion here


def create_eNodeBs():
    pass


def create_bbox():
    pass


if __name__ == '__main__':
    unittest.main()
