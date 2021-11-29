from typing import List
from .models import CarInfo, TimeLocation
import xmltodict

def extract_car_time_locations_from_fcd_file(fcd_file: str) -> List[CarInfo]:
    """Reads fcd SUMO output file and maps it into car-info objects.
    """
    
    with open(fcd_file, 'rb') as f:
        xml_data = xmltodict.parse(f.read())

    raw_cars_times = xml_data['fcd-export']['timestep'] # list

    cars: List[CarInfo] = []

    for timestep_cars_item in raw_cars_times:
        timestep = float(timestep_cars_item['@time'])

        if 'vehicle' in timestep_cars_item.keys():
            cars_in_time = timestep_cars_item['vehicle']

            # It may happen that there is only one car in timestep...
            if type(cars_in_time) is list:
                for raw_car_info in cars_in_time:
                    add_time_location_to_car(timestep, cars, raw_car_info)
                    

            else:
                add_time_location_to_car(cars_in_time)
                
    return cars

def add_time_location_to_car(timestep: float, cars, raw_car_info: dict):
    car_id = raw_car_info['@id']
    pos_x = float(raw_car_info['@x'])
    pos_y = float(raw_car_info['@y'])

    time_location = TimeLocation(timestep, pos_x, pos_y)
    
    all_car_ids = list(map(lambda c: c.Id, cars))
    
    if car_id in all_car_ids:
        car = list(filter(lambda c: c.Id == car_id, cars))[0]
        
    else:
        car = CarInfo(car_id)
        cars.append(car)
    
    car.time_locations.append(time_location)
    
