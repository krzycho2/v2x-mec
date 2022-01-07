import unittest

from src.sumo.parse_fcd import parse_fcd_data_parallel


class MyTestCase(unittest.TestCase):
    def test_parse_fcd_data_parallel(self):
        fcd_file = 'test-files/test-fcd.xml'

        car_time_location_items = parse_fcd_data_parallel(fcd_file)
        expected_count = 30
        expected_each_time_count = 5
        expected_each_car_count = 6

        self.assertEqual(len(car_time_location_items), expected_count)

        timesteps = set(map(lambda item: item['time'], car_time_location_items))
        for timestep in timesteps:
            items_for_timestep = list(filter(lambda item: item['time'] == timestep, car_time_location_items))

            self.assertEqual(len(items_for_timestep), expected_each_time_count)

        car_ids = set(map(lambda item: item['car_id'], car_time_location_items))
        for car_id in car_ids:
            items_for_car_id = list(filter(lambda item: item['car_id'] == car_id, car_time_location_items))

            self.assertEqual(len(items_for_car_id), expected_each_car_count)


if __name__ == '__main__':
    unittest.main()
