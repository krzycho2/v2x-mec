import json
from math import ceil
from typing import List
from json import loads
from geohelpers import get_distance_on_map, read_coords_file_and_project

class eNodeB:
    def __init__(self, id: int, x: float, y: float) -> None:
        self.id = id
        self.x = x
        self.y = y

class MapSquare:
    eNodeB: eNodeB = None
    
    def __init__(self, center_x, center_y, size) -> None:
        self.center_x = center_x
        self.center_y = center_y
        self.size = size
        
    def assign_eNb(self, eNodeBs: List[eNodeB]):
        """Assigns eNB's id which is closest on map

        Args:
            enbs (List[eNb]): all eNBs
        """
        self.eNodeB = min(eNodeBs, key=lambda enb: get_distance_on_map(self.center_x, self.center_y, enb.x, enb.y))
    
def read_eNodeBs_from_file(eNodeBs_coords_file: str):
    eNodeBs_coords = read_coords_file_and_project(eNodeBs_coords_file)
    eNodeBs = []
    for index, bts in enumerate(eNodeBs_coords):
        eNodeBs.append(eNodeB(index, bts['x'], bts['y']))
        
    return eNodeBs

def read_boundary_box_coords(map_bbox_file: str):
    with open(map_bbox_file, 'r') as f:
        bbox_coords = json.load(f)

    required_keys = ['x0', 'x1', 'y0', 'y1']
    assert(all(k in bbox_coords for k in required_keys))
    return bbox_coords


def create_map_squares(map_bbox_file: str, square_size = 100):
    boundary_coords = read_boundary_box_coords(map_bbox_file)
    squares = create_squares(boundary_coords['x0'], boundary_coords['x1'], boundary_coords['y0'], boundary_coords['y1'], square_size)
    return squares

def assign_eNodeBs_to_map_squares(eNodeBs: List[eNodeB], MapSquares: List[MapSquare]):
    for MapSquare in MapSquares:
        MapSquare.assign_eNb(eNodeBs)
    
def create_squares(min_x, max_x, min_y, max_y, size) -> List[MapSquare]:
    delta_x = max_x - min_x
    delta_y = max_y - min_y
    
    MapSquares_count_x = ceil(delta_x / size)
    MapSquares_count_y = ceil(delta_y / size)
    
    MapSquares = []
    for i in range(MapSquares_count_x):
        for j in range(MapSquares_count_y):
            center_x = min_x + i * size + size / 2
            center_y = min_y + j * size + size / 2
            MapSquares.append(MapSquare(center_x, center_y, size))
            
    return MapSquares
        
    
        