from math import radians, cos, sin, asin, sqrt
import numpy as np
def distance(lon1: float, lat1: float, lon2: float, lat2: float):
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

def create_heat_map():
    pass



