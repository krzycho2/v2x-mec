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
        
    
        