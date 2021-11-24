import xmltodict

from cellarea import *
from models import TimeLocation, SimBoundary

def parse_fcd(fcd_file_path: str) -> dict:
    """
    Reads an fcd file (SUMO output file) and returns car infos and simulation boundary.

    Parameters
        fcd_file_path - path to a fcd file created by sumo

    Returns
        A tuple (dict: {car_id: list<TimeLocation>}, sim_boundary)
    """

    with open(fcd_file_path, 'rb') as f:
        xml_data = f.read()

    data = xmltodict.parse(xml_data)

    raw_cars_times = data['fcd-export']['timestep'] # list

    car_infos = {}
    sim_boundary = SimBoundary()

    for time_cars_item in raw_cars_times:
        time = float(time_cars_item['@time'])

        if 'vehicle' in time_cars_item.keys():
            cars_in_time_raw = time_cars_item['vehicle']

            if type(cars_in_time_raw) is list:
                for raw_car_info in cars_in_time_raw:
                    car_id = raw_car_info['@id']
                    pos_x = float(raw_car_info['@x'])
                    pos_y = float(raw_car_info['@y'])

                    if not car_id in car_infos.keys():
                        car_infos[car_id] = []

                    # car_infos[car_id][time] = (pos_x, pos_y)
                    time_location = TimeLocation(time, pos_x, pos_y)
                    car_infos[car_id].append(time_location)

                    sim_boundary.check_set_value('x', pos_x)
                    sim_boundary.check_set_value('y', pos_y)

            else:
                car_id = cars_in_time_raw['@id']
                pos_x = float(cars_in_time_raw['@x'])
                pos_y = float(cars_in_time_raw['@y'])

                if not car_id in car_infos.keys():
                    car_infos[car_id] = []

                time_location = TimeLocation(time, pos_x, pos_y)
                car_infos[car_id].append(time_location)

                sim_boundary.check_set_value('x', pos_x)
                sim_boundary.check_set_value('y', pos_y)
                
    return (car_infos, sim_boundary)