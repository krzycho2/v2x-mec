import unittest

from src.sumo.parse_fcd import load_fcd_data_parallel


class ParseFcdTests(unittest.TestCase):
    def test_load_fcd_data_parallel(self):
        fcd_file = 'test-files/test-fcd.xml'
        expected_cars = 5
        expected_timesteps = 6
        expected_time_locations_count = 30

        car_time_locations = load_fcd_data_parallel(fcd_file)

        self.assertEqual(expected_time_locations_count, len(car_time_locations))

        car_ids = set([car_time_location[1] for car_time_location in car_time_locations])
        self.assertEqual(expected_cars, len(car_ids))

        for car_id in car_ids:
            car_time_locations_for_car = list(filter(lambda car_time_location: car_time_location[1] == car_id, car_time_locations))
            self.assertEqual(expected_timesteps, len(car_time_locations_for_car))


if __name__ == '__main__':
    unittest.main()
