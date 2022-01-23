from typing import List


class Position2d:
    x: float
    y: float

    def __init__(self, x, y) -> None:
        self.x = float(x)
        self.y = float(y)


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

    def get_all_vertices(self) -> list:
        return [Position2d(self.x_min, self.y_min), Position2d(self.x_max, self.y_min),
                Position2d(self.x_max, self.y_max), Position2d(self.x_min, self.y_max)]

    def get_lines(self) -> list:
        return [[Position2d(self.x_min, self.y_min), Position2d(self.x_max, self.y_min)],
                [Position2d(self.x_min, self.y_min), Position2d(self.x_min, self.y_max)],
                [Position2d(self.x_max, self.y_min), Position2d(self.x_max, self.y_max)],
                [Position2d(self.x_min, self.y_max), Position2d(self.x_max, self.y_max)]]


class TimeLocation:
    time: float
    location: Position2d

    def __init__(self, time, x, y) -> None:
        self.time = float(time)
        self.location = Position2d(x, y)


class CarInfo:
    Id: str
    time_locations: List[TimeLocation]

    def __init__(self, id: str, time_locations: List[TimeLocation] = None) -> None:
        if time_locations is None:
            time_locations = []

        self.Id = id
        self.time_locations = time_locations
