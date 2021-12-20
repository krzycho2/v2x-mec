from typing import List
from cellarea import Cell, create_cells, get_avg_arrival_freq, get_cell_by_location, get_max_arrival_freq, get_min_arrival_freq, get_sum_arrival_count
from src.models.map_time_models import TimeLocation
from v2x.cars import CarInfo
from v2x.mec import Mec
from parsefcd import parse_fcd

DEFAULT_CELL_LENGTHS = [300, 600, 900]

class Uct:
    mec_id_pair: tuple
    time: float
    
    def __init__(self, mec_id_pair: tuple, time: float) -> None:
        self.mec_id_pair = mec_id_pair
        self.time = time

def calculate_uct_stats(car_time_locations: List[CarInfo], mecs: List[Mec]) -> dict:
    """Finds UCTs and calculates statistics for them.

    Returns:
        dict: UCT statistics TODO
    """
    
# ----------- OLD CODE -----------------------------------------------------------
# def calculate_uct_stats(fcd_file_path: str, cell_lengths = DEFAULT_CELL_LENGTHS):
#     car_infos, sim_boundary = parse_fcd(fcd_file_path) # car_infos: dicts {car_id: time_locations}
    
#     for cell_length in cell_lengths:
#         cells_per_mec = (cell_length / 300)**2
#         cells = create_cells(cell_length, sim_boundary.min_x, sim_boundary.min_y, sim_boundary.max_x, sim_boundary.max_y)
#         transfers = calculate_transfers(car_infos, cells)
#         cells = allocate_transfers_to_cells(transfers, cells)
        
#         print_stats(cells, cell_length, cells_per_mec)
        
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

def print_stats(cells: List[Cell], cell_length: float, cells_per_mec: float):
    print(f'Cell length: {cell_length}, cells per mec: {cells_per_mec}')
    print(f'Max UCT/s: {get_max_arrival_freq(cells)}')
    print(f'Min UCT/s: {get_min_arrival_freq(cells)}')
    print(f'AVG UCT/s: {get_avg_arrival_freq(cells)}')
    print(f'All UCTs: {get_sum_arrival_count(cells)}')

