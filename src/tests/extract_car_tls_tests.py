import unittest

from src.v2x.cars import extract_car_time_locations_from_fcd_file


class ExtractCarTimeLocationsTests(unittest.TestCase):
    def test1(self):
        fcd_file = '../v2x/test-fcd.xml'
        expected_cars = 5
        expected_timesteps = 6
        expected_time_locations = 6
        
        cars = extract_car_time_locations_from_fcd_file(fcd_file)
        
        car_ids = list(map(lambda c: c.Id, cars))
        self.assertEqual(expected_cars, len(car_ids))
        
        timesteps = list(map(lambda ts: ts.time, cars[0].time_locations))
        self.assertEqual(expected_timesteps, len(timesteps))
        
        self.assertTrue(all(map(lambda c: len(c.time_locations) == expected_time_locations, cars)))


if __name__ == '__main__':
    unittest.main()