import math
from cellarea import Cell

class CarInfo():
    def __init__(self, car_id, time_locations: list):
        self.car_id = car_id
        self.time_locations = time_locations

class TimeLocation():
    def __init__(self, time: float, x: float, y: float, cell: Cell = None):
        self.time = time
        self.x = x
        self.y = y
        self.cell = cell

class CarLocation():
    def __init__(self, car_id: str, x: float, y: float):
        self.car_id = car_id
        self.x = x
        self.y = y

class SimBoundary():
    def __init__(self):
        self.min_x = math.inf
        self.min_y = math.inf
        self.max_x = 0
        self.max_y = 0

    def check_set_value(self, xy: str, possible_value: float):
        if xy == 'x':
            self.check_possible_min_x(possible_value)
            self.check_possible_max_x(possible_value)

        if xy == 'y':
            self.check_possible_min_y(possible_value)
            self.check_possible_max_y(possible_value)

    def check_possible_min_x(self, possible_min_x: float):
        if possible_min_x < self.min_x:
            self.min_x = possible_min_x

    def check_possible_min_y(self, possible_min_y):
        if possible_min_y < self.min_y:
            self.min_y = possible_min_y

    def check_possible_max_x(self, possible_max_x):
        if possible_max_x > self.max_x:
            self.max_x = possible_max_x

    def check_possible_max_y(self, possible_max_y):
        if possible_max_y > self.max_y:
            self.max_y = possible_max_y

def get_sim_boundary(all_x: list, all_y: list):
    pass