from typing import List

from lxml import etree
import time
import xmltodict
from lxml.etree import XMLParser, parse
import multiprocessing as mp
from src.models.map_time_models import CarInfo, TimeLocation
import numpy as np

def select_items_for_car(car_id: str, all_items: List[dict]):
    return list(filter(lambda item: item['car_id'] == car_id, all_items))


def select_items_for_car2(car_id: str, all_items: List[List]):
    return list(filter(lambda item: item[1] == car_id, all_items))

def select_items_for_car_numpy(car_id: str, all_items: List[List]):
    filtr = np.asarray([car_id])
    arr = np.array(all_items)
    return arr[np.in1d(arr[:, 1], filtr)]

def extract_time_location_for_car(items_for_car: List[dict]):
    car = CarInfo(items_for_car[0]['car_id'])
    car.time_locations.extend([TimeLocation(item['time'], item['x'], item['y']) for item in items_for_car])
    return car


def extract_time_location_for_car2(items_for_car: List[List]):
    car = CarInfo(items_for_car[0][1])
    car.time_locations.extend([TimeLocation(item[0], item[2], item[3]) for item in items_for_car])
    return car


def extract_car_time_locations_parallel(car_time_location_items: List[dict]) -> List[CarInfo]:
    print('Extracting car_time_location items to CarInfo objects')
    start_time = time.time()
    car_ids = set(map(lambda item: item['car_id'], car_time_location_items))
    cars: List[CarInfo] = []

    pool = mp.Pool(mp.cpu_count())
    results = pool.map(extract_time_location_for_car,
                       [select_items_for_car(car_id, car_time_location_items) for car_id in car_ids])

    end_time = time.time()
    print('Extracting car_time_location items to CarInfo objects parallel took:', end_time - start_time)

    return results


def extract_car_time_locations_parallel2(car_time_location_items: List[List]) -> List[CarInfo]:
    print('Extracting car_time_location items to CarInfo objects')
    start_time = time.time()
    car_ids = set(map(lambda item: item[1], car_time_location_items))

    pool = mp.Pool(mp.cpu_count())
    results = pool.map(extract_time_location_for_car2,
                       [select_items_for_car2(car_id, car_time_location_items) for car_id in car_ids])

    pool.close()
    pool.join()

    end_time = time.time()
    print('Extracting car_time_location items to CarInfo objects parallel took:', end_time - start_time)

    return results


def extract_time_location_for_car3(car_id: str, all_items: List[List]):
    car = CarInfo(car_id)
    items_for_car = select_items_for_car2(car_id, all_items)
    car.time_locations.extend([TimeLocation(item[0], item[2], item[3]) for item in items_for_car])
    return car


def extract_car_time_locations_parallel3(car_time_location_items: List[List]) -> List[CarInfo]:
    print('Extracting car_time_location items to CarInfo objects')
    start_time = time.time()
    car_ids = set(map(lambda item: item[1], car_time_location_items))

    pool = mp.Pool(mp.cpu_count())
    # results = pool.map(extract_time_location_for_car2,
    #                    [select_items_for_car2(car_id, car_time_location_items) for car_id in car_ids])

    # results = [pool.apply(extract_time_location_for_car3, args=(car_id, car_time_location_items)) for car_id in car_ids]
    results = pool.starmap(extract_time_location_for_car3, [(car_id, car_time_location_items) for car_id in car_ids])

    pool.close()
    pool.join()

    end_time = time.time()
    print('Extracting car_time_location items to CarInfo objects parallel took:', end_time - start_time)

    return results


def group_items_per_car_parallel(car_time_location_items: List[List]) -> List[List[List]]:
    print('Grouping car_time_location items per each car')
    start_time = time.time()
    car_ids = set(map(lambda item: item[1], car_time_location_items))

    pool = mp.Pool(mp.cpu_count())
    results = pool.starmap(select_items_for_car2, [(car_id, car_time_location_items) for car_id in car_ids])
    pool.close()
    pool.join()

    end_time = time.time()
    print('Grouping car_time_location items per each car took:', end_time - start_time)
    return results


def extract_car_time_locations_parallel4(car_time_location_items: List[List]) -> List[CarInfo]:
    print('Extracting car_time_location items to CarInfo objects')
    start_time = time.time()
    car_ids = set(map(lambda item: item[1], car_time_location_items))

    lists_of_items_per_car = group_items_per_car_parallel(car_time_location_items)
    pool = mp.Pool(mp.cpu_count())
    cars = pool.starmap(extract_time_location_for_car2, lists_of_items_per_car)

    pool.close()
    pool.join()

    return cars


def extract_car_time_locations2(car_time_location_items: List[dict]) -> List[CarInfo]:
    """
    Summary:
        Extracting car_time_location items to CarInfo objects.
    Args:
        car_time_location_items:

    Returns:

    """
    print('Extracting car_time_location items to CarInfo objects')
    start_time = time.time()
    car_ids = set(map(lambda item: item['car_id'], car_time_location_items))
    cars: List[CarInfo] = []

    for car_id in car_ids:
        items_for_car_id = list(filter(lambda item: item['car_id'] == car_id, car_time_location_items))

        car = CarInfo(car_id)
        car.time_locations.extend([TimeLocation(item['time'], item['x'], item['y']) for item in items_for_car_id])
        cars.append(car)

    end_time = time.time()
    print('Extracting car_time_location items to CarInfo objects took:', end_time - start_time)

    return cars


def extract_car_time_locations(car_time_location_items: List[List]) -> List[CarInfo]:
    cars: List[CarInfo] = []
    for car_time_location in car_time_location_items:
        car_id = car_time_location[1]
        time_stamp = car_time_location[0]
        x = car_time_location[2]
        y = car_time_location[3]

        time_location = TimeLocation(time_stamp, x, y)

        all_car_ids = list(map(lambda c: c.Id, cars))

        if car_id in all_car_ids:
            car = next(filter(lambda c: c.Id == car_id, cars))

        else:
            car = CarInfo(car_id)
            cars.append(car)

        car.time_locations.append(time_location)

    return cars


def extract_car_time_locations_from_fcd_file(fcd_file: str) -> List[CarInfo]:
    """Reads fcd SUMO output file and maps it into car-info objects.
    """

    print("Extracting cars' location and time...")
    
    with open(fcd_file, 'rb') as f:
        xml_data = xmltodict.parse(f.read())

    raw_cars_times = xml_data['fcd-export']['timestep'] # list

    cars: List[CarInfo] = []
    timesteps_count = len(raw_cars_times)
    print('ALl Timesteps:', timesteps_count)
    print('cars:')
    for index, timestep_cars_item in enumerate(raw_cars_times):
        timestep = float(timestep_cars_item['@time'])

        if 'vehicle' in timestep_cars_item.keys():
            cars_in_time = timestep_cars_item['vehicle']

            # It may happen that there is only one car in timestep...
            if type(cars_in_time) is list:
                for raw_car_info in cars_in_time:
                    add_time_location_to_car(timestep, cars, raw_car_info)
                    
            else:
                add_time_location_to_car(timestep, cars, cars_in_time)

        if timestep % int(1e5) == 0:
            print(f'Timestep {timestep} of {timesteps_count}')

    return cars


def add_time_location_to_car(timestep: float, cars: List[CarInfo], raw_car_info: dict):
    car_id = raw_car_info['@id']
    pos_x = float(raw_car_info['@x'])
    pos_y = float(raw_car_info['@y'])

    time_location = TimeLocation(timestep, pos_x, pos_y)
    
    all_car_ids = list(map(lambda c: c.Id, cars))
    
    if car_id in all_car_ids:
        car = next(filter(lambda c: c.Id == car_id, cars))
        
    else:
        car = CarInfo(car_id)
        cars.append(car)
    
    car.time_locations.append(time_location)


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
