import xmltodict
from models import CarInfo, CarLocation

def parse_fcd(fcd_file_path: str) -> dict:
    """
    Returns a dict: {time: list of cars (with theirs infos) in this time}
    """

    with open('fcd_dump_mini.xml', 'rb') as f:
        xml_data = f.read()

    data = xmltodict.parse(xml_data)

    raw_cars_times = data['fcd-export']['timestep'] # list

    cars_in_time = {} # dict: {time: cars_list_in_this_time}
    for time_cars_item in raw_cars_times:
        time = float(time_cars_item['@time'])
        cars_in_time[time] = []

        cars_in_time_raw = time_cars_item['vehicle']
        if type(cars_in_time_raw) is list:
            for raw_car_info in cars_in_time_raw:
                car_id = raw_car_info['@id']
                pos_x = raw_car_info['@x']
                pos_y = raw_car_info['@y']
                car_info = CarInfo(car_id, pos_x, pos_y)

                cars_in_time[time].append(car_info)

        else:
            car_id = cars_in_time_raw['@id']
            pos_x = cars_in_time_raw['@x']
            pos_y = cars_in_time_raw['@y']
            car_info = CarInfo(car_id, pos_x, pos_y)

            cars_in_time[time].append(car_info)

    return cars_in_time

def get_location_events(fcd_file_path: str) -> list:
    """
    Returns a list of dicts; dict - {time: CarLocation}
    """

    with open(fcd_file_path, 'rb') as f:
        xml_data = f.read()

    data = xmltodict.parse(xml_data)

    raw_cars_times = data['fcd-export']['timestep'] # list

    events = [] # list of dicts; dict: {time: CarLocation}
    for time_cars_item in raw_cars_times:
        time = float(time_cars_item['@time'])

        if 'vehicle' in time_cars_item.keys():
            cars_in_time_raw = time_cars_item['vehicle']
            if type(cars_in_time_raw) is list:
                for raw_car_info in cars_in_time_raw:
                    car_id = raw_car_info['@id']
                    pos_x = float(raw_car_info['@x'])
                    pos_y = float(raw_car_info['@y'])
                    
                    car_location = CarLocation(car_id, pos_x, pos_y)
                    events.append({time:car_location})


            else:
                car_id = cars_in_time_raw['@id']
                pos_x = float(cars_in_time_raw['@x'])
                pos_y = float(cars_in_time_raw['@y'])
                car_location = CarLocation(car_id, pos_x, pos_y)

                events.append({time:car_location})

    return events

def count_cell_transfers(transferred_cells_ids: list):
    transfers_counts = {}
    for cell_id in transferred_cells_ids:
        if not cell_id in transfers_counts.keys():
            transfers_counts[cell_id] = 0
        
        transfers_counts[cell_id] += 1
        
    return transfers_counts

def find_cell_transfers(car_location_events: list, cells: list):
    """
    Finds cells' transfers in car_location - time events.

    Parameters:
        car_location_events - list of dicts: {time:CarLocation}
        cells - list of cells
    Returns:
        List of cells' ids for which transfer occured
    """
    transferred_cells = []
    for event_a in car_location_events:
        for event_b in car_location_events:

            a_time = list(event_a.keys())[0]
            b_time = list(event_b.keys())[0]

            a_car_location = list(event_a.values())[0]
            b_car_location = list(event_b.values())[0]

            if a_car_location.car_id == b_car_location.car_id:
                try:
                    cell_a = get_cell_by_location(a_car_location.x, a_car_location.y, cells)
                except:
                    print('Problem')
                try:
                    cell_b = get_cell_by_location(b_car_location.x, b_car_location.y, cells)
                except:
                    print('problem')

                if a_time == b_time + 1 and are_cells_neighbors(cell_a, cell_b):
                    if cell_a.cell_id != cell_b.cell_id:
                        transferred_cells.append(cell_a.cell_id)

    return transferred_cells

def find_sim_boundary(car_location_events: list) -> tuple:
    """
    Returns tuple (min_x, min_y, max_x, max_y) of sim boundary
    """
    all_x = []
    all_y = []
    for event in car_location_events:
        location = list(event.values())[0]
        all_x.append(location.x)
        all_y.append(location.y)

    return (min(all_x), min(all_y), max(all_x), max(all_y))
