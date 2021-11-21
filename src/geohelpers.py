from math import radians, cos, sin, asin, sqrt, ceil
from pyproj import Proj
from typing import List


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

def get_distance_on_map(x1, y1, x2, y2):
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
        
    projected_coords = list()
    
    for coords in coords_lines:
        lat, long = coords.split(',')
        xy_dict = dict()
        xy_dict['x'], xy_dict['y'] = project_coords(long, lat)
        projected_coords.append(xy_dict)
        
    return projected_coords

def project_coords(longitude: float, latitude: float):
    p = Proj(proj='utm', zone=32, eelps='WGS84', preserve_units=False)
    return p(longitude, latitude)