from typing import List
from map_time_models import TimeLocation

class CarInfo:
    Id: int
    time_locations: List[TimeLocation]
    
    def __init__(self, id: int, time_locations: List[TimeLocation]) -> None:
        self.If = id
        self.time_locations = time_locations

def extract_cars(time_locations: List[TimeLocation]) -> List[CarInfo]:
    """Gets list of time-location objects (aquired from sumo FCD output file) and groups it into list of cars and their time-locations.
    """
    # TODO
    pass