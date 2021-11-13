from math import radians, cos, sin, asin, sqrt
import numpy as np
from pyproj import Proj
from typing import List

BTS_COORDS_FILE_PATH = '/home/chris/Documents/STUDIA/Praca_mgr/Symulacje/v2x-mec/bts/bts-coords.txt'
BTS_MAP_VERTEXES_FILE_PATH = '/home/chris/Documents/STUDIA/Praca_mgr/Symulacje/v2x-mec/bts/square-tops.txt'

def distance_on_earth(lon1: float, lat1: float, lon2: float, lat2: float):
    """
    Calculates distance in kilometers between two points on earth.
    From https://www.geeksforgeeks.org/program-distance-two-points-earth/
    """
    lon1 = radians(lon1)
    lon2 = radians(lon2)
    lat1 = radians(lat1)
    lat2 = radians(lat2)
      
    # Haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
 
    c = 2 * asin(sqrt(a))
    
    # Radius of earth in kilometers. Use 3956 for miles
    r = 6371
      
    # calculate the result
    return(c * r)

def distance(x1, y1, x2, y2):
    return sqrt( (x1 - x2)**2 + (y1-y2)**2)

def read_coords_file_and_project(coords_file: str) -> List[dict]:
    """Reads and transforms (projects) coordinates from file.

    Args:
        coords_file (str): path to the file with pairs (longitude,latitude)

    Returns:
        List of dicts with keys 'x' and 'y'
    """
    
    with open(coords_file, 'r') as f:
        coords_lines = f.readlines()
        
    p = Proj(proj='utm', zone=10, eelps='WGS84', preserve_units=False)
    
    projected_coords = list()
    
    for coords in coords_lines:
        long, lat = coords.split(',')
        xy_dict = dict()
        xy_dict['x'], xy_dict['y'] = p(long, lat)
        projected_coords.append(xy_dict)
        
    return projected_coords

def create_bts_boundaries() -> list:
    """
    1. Projekcja współrzędnych btsów i mapy
    1. Podzielić mapę na siatkę 50x50 (2500 kwadratów) i uzyskać jego współrzędne
    2. Dla każdego z kwadratu obliczyć odległość od każdego z btsów
    """
    
    bts_coords = read_coords_file_and_project(BTS_COORDS_FILE_PATH)
    map_vertexes = read_coords_file_and_project(BTS_MAP_VERTEXES_FILE_PATH)
    
    # Divide the map into 50x50 grid
    n_rows = 50
    n_columns = 50
    
    
    




