from typing import List

class Point:
    x: float
    y: float
    grid_density_x: float
    grid_density_y: float
    
    def __init__(self, x: float, y: float) -> None:
        self.x = x
        self.y = y
        
        self.grid_density_x = 50
        self.grid_density_y = 50
        
class TimeLocation:
    time: float
    location: Point
    
    def __init__(self, time: float, x: float, y: float) -> None:
        self.time = time
        self.location = Point(x, y)

class CarInfo:
    Id: str
    time_locations: List[TimeLocation] = []
    
    def __init__(self, id: str) -> None:
        self.Id = id
        self.time_locations = []

        
class eNodeB:
    Id: int
    location: Point
    boundary_points: List[Point]
    
    def __init__(self, id: int, location: Point, boundary_points: List[Point]) -> None:
        self.Id = id
        self.location = location
        self.boundary_points = boundary_points
        
class Mec:
    Id: int
    boundary_points: List[Point]
    
    def __init__(self, mec_id: int, boundary_points: List[Point]) -> None:
        self.Id = mec_id
        self.boundary_points = boundary_points
        
    def include_eNodeB(self, eNodeB: eNodeB):
        "Incorporates eNodeB range to Mec boundary_points range."
        pass
    
    
        
