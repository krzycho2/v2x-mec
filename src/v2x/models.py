from typing import List


# TODO: Move to map_time_models
class Position2d:
    x: float
    y: float
    grid_density_x: float
    grid_density_y: float

    def __init__(self, x: float, y: float) -> None:
        self.x = x
        self.y = y

        self.grid_density_x = 50
        self.grid_density_y = 50


class BoundaryBox:
    x_min: float
    x_max: float
    y_min: float
    y_max: float

    def __init__(self, x_min: float, y_min: float, x_max: float, y_max: float) -> None:
        self.x_min = x_min
        self.x_max = x_max
        self.y_min = y_min
        self.y_max = y_max

    def get_all_vertexes(self) -> list:
        return [Position2d(self.x_min, self.y_min), Position2d(self.x_max, self.y_min),
                Position2d(self.y_max, self.x_min), Position2d(self.x_max, self.y_max)]

    def get_lines(self) -> list:
        return [[Position2d(self.x_min, self.y_min), Position2d(self.x_max, self.y_min)],  # lower
                [Position2d(self.x_min, self.y_min), Position2d(self.x_min, self.y_max)],  # left
                [Position2d(self.x_max, self.y_min), Position2d(self.x_max, self.y_max)],   # right
                [Position2d(self.x_min, self.y_max), Position2d(self.x_max, self.y_max)]]   # up


class TimeLocation:
    time: float
    location: Position2d

    def __init__(self, time: float, x: float, y: float) -> None:
        self.time = time
        self.location = Position2d(x, y)


# TODO: Move to v2x_models
class CarInfo:
    Id: str
    time_locations: List[TimeLocation]

    def __init__(self, id: str, time_locations=[]) -> None:
        self.Id = id
        self.time_locations = time_locations


class eNodeB:
    Id: int
    location: Position2d
    boundary_points: List[Position2d]
    assigned_mec_id: int

    def __init__(self, id: int, x: float, y: float, assigned_mec_id=None) -> None:
        self.Id = id
        self.location = Position2d(x, y)
        self.boundary_points = []
        self.assigned_mec_id = assigned_mec_id


class Mec:
    Id: int
    boundary_points: List[Position2d]

    def __init__(self, mec_id: int, boundary_points: List[Position2d] = []) -> None:
        self.Id = mec_id
        self.boundary_points = boundary_points

    def include_eNodeB(self, eNodeB: eNodeB):
        "Incorporates eNodeB range to Mec boundary_points range."
        pass
