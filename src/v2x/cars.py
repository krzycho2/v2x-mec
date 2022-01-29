import time
from typing import List
from lxml.etree import XMLParser, parse
from src.models.map_time_models import CarInfo, TimeLocation


# Legacy
def extract_cars_lxml(fcd_file):
    print('Extracting cars and timeLocations...')

    print('Loading fcd...')
    start_time = time.time()
    # with open(fcd_file, 'rb') as f:
    #     xml_data = etree.parse(f)

    p = XMLParser(huge_tree=True)
    xml_data = parse(fcd_file, parser=p)

    end_time = time.time()
    load_time = end_time - start_time
    print('Loading fcd took:', load_time)

    fcd_export = xml_data.getroot()
    cars: List[CarInfo] = []

    timesteps_count = len(fcd_export.getchildren())
    print('All timesteps:', timesteps_count)

    print('Parsing fcd...')
    start_time = time.time()

    for index, timestep_cars_item in enumerate(fcd_export):
        time_stamp = float(timestep_cars_item.get('time'))

        for raw_car_info in timestep_cars_item:
            car_id = raw_car_info.get('id')
            pos_x = raw_car_info.get('x')
            pos_y = raw_car_info.get('y')

            time_location = TimeLocation(time_stamp, pos_x, pos_y)

            all_car_ids = list(map(lambda c: c.Id, cars))

            if car_id in all_car_ids:
                car = next(filter(lambda c: c.Id == car_id, cars))

            else:
                car = CarInfo(car_id)
                cars.append(car)

            car.time_locations.append(time_location)

        if index % 1000 == 0:
            print('Timestep:', index)

    end_time = time.time()
    parse_time = end_time - start_time
    print('Parsing fcd took:', parse_time)

    print('Summary time:', load_time + parse_time)
    return cars
