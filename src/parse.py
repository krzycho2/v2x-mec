import time
import pickle
from itertools import groupby
import argparse

from cellarea import *
from models import TimeLocation, SimBoundary

from sumo.parsefcd import parse_fcd


# def parse_fcd(fcd_file_path: str) -> dict:
#     """
#     Returns car infos and simulation boundary.

#     Parameters
#         fcd_file_path - path to a fcd file created by sumo

#     Returns
#         A tuple (dict: {car_id: list<TimeLocation>}, sim_boundary)
#     """

#     with open(fcd_file_path, 'rb') as f:
#         xml_data = f.read()

#     data = xmltodict.parse(xml_data)

#     raw_cars_times = data['fcd-export']['timestep'] # list

#     car_infos = {}
#     sim_boundary = SimBoundary()

#     for time_cars_item in raw_cars_times:
#         time = float(time_cars_item['@time'])

#         if 'vehicle' in time_cars_item.keys():
#             cars_in_time_raw = time_cars_item['vehicle']

#             if type(cars_in_time_raw) is list:
#                 for raw_car_info in cars_in_time_raw:
#                     car_id = raw_car_info['@id']
#                     pos_x = float(raw_car_info['@x'])
#                     pos_y = float(raw_car_info['@y'])

#                     if not car_id in car_infos.keys():
#                         car_infos[car_id] = []

#                     # car_infos[car_id][time] = (pos_x, pos_y)
#                     time_location = TimeLocation(time, pos_x, pos_y)
#                     car_infos[car_id].append(time_location)

#                     sim_boundary.check_set_value('x', pos_x)
#                     sim_boundary.check_set_value('y', pos_y)

#             else:
#                 car_id = cars_in_time_raw['@id']
#                 pos_x = float(cars_in_time_raw['@x'])
#                 pos_y = float(cars_in_time_raw['@y'])

#                 if not car_id in car_infos.keys():
#                     car_infos[car_id] = []

#                 time_location = TimeLocation(time, pos_x, pos_y)
#                 car_infos[car_id].append(time_location)

#                 sim_boundary.check_set_value('x', pos_x)
#                 sim_boundary.check_set_value('y', pos_y)

     

#     return (car_infos, sim_boundary)

def calculate_transfers(car_infos: dict, cells: list):
    transfers = [] # list of cell_id 
    for car_id in car_infos.keys():
        time_locations = car_infos[car_id]
        time_locations[0].cell = get_cell_by_location(time_locations[0].x, time_locations[0].y, cells)

        for i in range(len(time_locations) - 1 ):
            tl_a, tl_b = time_locations[i:i+2]
            tl_b.cell = get_cell_by_location(tl_b.x, tl_b.y, cells)

            if tl_a.cell.cell_id != tl_b.cell.cell_id:
                # transfers.append(tl_a.cell.cell_id)
                transfers.append({'time': tl_a.time, 'car_id': car_id, 'source_cell_id': tl_a.cell.cell_id, 'dest_cell_id': tl_b.cell.cell_id, 'location_a': [tl_a.x, tl_a.y], 'location_b': [tl_b.x, tl_b.y]})

    return transfers

def get_transfers_counts(transfers: dict, sourceDest: str = 'source'):
    key = ''
    if sourceDest == 'source':
        key = 'source_cell_id'
    else:
        key = 'dest_cell_id'

    cell_ids = [t[key] for t in transfers]
    cell_ids.sort()
    id_count_dicts = [{key: key, 'count': len(list(group))} for key, group in groupby(cell_ids)]

    return sorted(id_count_dicts, key=lambda k: k['count'],reverse=True)

def allocate_transfers_to_cells(transfers: list, cells: list) -> list:
    '''
    Returns list of cells with allocated transfers connected with them.
    
    Parameters
        transfers - list of dicts {time, car_id, source_cell_id, dest_cell_id, location_a, location_b}

        cells - list of cells
    '''

    for transfer in transfers:
        time = transfer['time']
        cell_arrival = next((cell for cell in cells if cell.cell_id == transfer['dest_cell_id']), None)
        cell_departure = next((cell for cell in cells if cell.cell_id == transfer['source_cell_id']), None)

        # Elements in cells are automatically updated, because these are references
        cell_arrival.transfers.append({'time': time, 'inOut': 'in'})
        cell_departure.transfers.append({'time': time, 'inOut': 'out'})

    return cells

def calculate(fcd_file_path: str, cell_length = 300) -> list:
    
    print('Plik fcd: ', fcd_file_path)

    t0 = time.perf_counter()
    
    car_infos, sim_boundary = parse_fcd(fcd_file_path) # car_infos: dicts {car_id: time_locations}
    cells = create_cells(cell_length, sim_boundary.min_x, sim_boundary.min_y, sim_boundary.max_x, sim_boundary.max_y)
    transfers = calculate_transfers(car_infos, cells)
    cells = allocate_transfers_to_cells(transfers, cells)
    
    t1 = time.perf_counter()

    print('Czas obliczeń: ', t1-t0)

    return cells

def calc_all(fcd_file_path: str):
    car_infos, sim_boundary = parse_fcd(fcd_file_path) # car_infos: dicts {car_id: time_locations}
    for cell_length in [300, 600, 900]:
        cells_per_mec = (cell_length / 300)**2
        cells = create_cells(cell_length, sim_boundary.min_x, sim_boundary.min_y, sim_boundary.max_x, sim_boundary.max_y)
        transfers = calculate_transfers(car_infos, cells)
        cells = allocate_transfers_to_cells(transfers, cells)
        print(f'Cell length: {cell_length}, cells per mec: {cells_per_mec}')
        print(f'Max UCT/s: {get_max_arrival_freq(cells)}')
        print(f'Min UCT/s: {get_min_arrival_freq(cells)}')
        print(f'AVG UCT/s: {get_avg_arrival_freq(cells)}')
        print(f'All UCTs: {get_sum_arrival_count(cells)}')



# file = 'fcd_dump_mini.xml'
# calculate(file)






# if __name__ == '__main__':
#     parser = argparse.ArgumentParser()
#     parser.add_argument('path')
#     args = parser.parse_args()

#     fsd_file_path = args.path
#     print(calculate(fsd_file_path))

