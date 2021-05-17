import math

class SquareCellArea():
    def __init__(self, length: float, center_x: float, center_y: float):
            self.length = length
            self.center_x = center_x
            self.center_y = center_y

    def get_min_x(self) -> float:
        return self.center_x - 0.5*self.length 

    def get_min_y(self) -> float:
        return self.center_y - 0.5*self.length

    def get_max_x(self) -> float:
        return self.center_x + 0.5*self.length

    def get_max_y(self) -> float:
        return self.center_y + 0.5*self.length

    def is_point_in_area(self, point_x: float, point_y: float) -> bool:
        return point_x >= self.get_min_x() and point_x < self.get_max_x() and point_y >= self.get_min_y() and point_y < self.get_max_y()


class CircleCellArea():
    def __init__(self, radius, center_x, center_y):
        self.radius = radius
        self.center_x = center_x
        self.center_y = center_y

class Cell():
    def __init__(self, cell_id: int, cell_area: SquareCellArea):
        self.cell_id = cell_id
        self.cell_area = cell_area
        self.transfers = [] # transfer: {time: float, inOut: str}

    def get_total_time(self) -> float:
        all_times = map(lambda transfer: transfer['time'], self.transfers)
        return max(list(all_times))

    def get_cars_arrival_count(self) -> int:
        return len(list(filter(lambda transfer: transfer['inOut'] == 'in', self.transfers)))

    def get_cars_arrival_frequency(self) -> float:
        if len(self.transfers) == 0:
            return 0
        else:
            return self.get_cars_arrival_count() / self.get_total_time()

    def get_cars_departures_count(self) -> int:
        return len(list(filter(lambda transfer: transfer['inOut'] == 'out', self.transfers)))

    def get_cars_departures_frequency(self) -> float:
        if len(self.transfers) == 0:
            return 0
        else:
            return self.get_cars_departures_count() / self.get_total_time()

    def get_cars_inside_count_in_time(self) -> list:
        '''Return list of dicts {'time', 'count'}'''
        counts = []

        # Init state
        if self.transfers[0]['inOut'] == 'in':
            counts.append({'time': self.transfers[0]['time'], 'count': 1})

        else:
            counts.append({'time': self.transfers[0]['time'], 'count': 0})

        for i in range(1, len(self.transfers)):
            transfer = self.transfers[i]
            last = self.transfers[i-1]

            if self.transfers[0]['inOut'] == 'in':
                counts.append({'time': transfer['time'], 'count': last['time'] + 1})

            else:
                counts.append({'time': transfer['time'], 'count': last['time'] - 1})

        return counts

    def get_avg_cars_inside_count(self) -> float:
        counts_times = self.get_cars_inside_count_in_time()
        counts = map((lambda ct: ct['count']), counts_times)
        return counts / len(self.transfers)

    def get_max_cars_inside_count(self) -> float:
        counts_times = self.get_cars_inside_count_in_time()
        counts = map((lambda ct: ct['count']), counts_times)

        return max(counts)

def create_cells(square_length: float, min_x: float, min_y: float, max_x: float, max_y: float) -> list:
    '''
    Returns list of cells.
    '''
    
    cells = []

    x_cells_count = math.ceil((max_x - min_x) / square_length)
    y_cells_count = math.ceil((max_y - min_y) / square_length)

    counter = 0
    for i in range(x_cells_count):
        for j in range(y_cells_count):
            cell_id = counter
            center_x = min_x + (0.5 + i) * square_length
            center_y = min_y + (0.5 + j) * square_length
            cells.append(Cell(cell_id, SquareCellArea(square_length, center_x, center_y)))

            counter += 1

    return cells

def are_cells_neighbors(cell1: Cell, cell2: Cell):
    area1 = cell1.cell_area
    area2 = cell2.cell_area

    return area1.get_max_x() == area2.get_min_x() \
        or area1.get_min_x() == area2.get_max_x() \
        or area1.get_max_y() == area2.get_min_y() \
        or area1.get_min_y() == area2.get_max_y()

def get_cell_by_location(x,y, cells: list) -> Cell:
    for cell in cells:
        if cell.cell_area.is_point_in_area(x, y):
            return cell
    raise Exception('Point not in any cell')

def get_max_arrival_count(cells):
    return max(map((lambda c: c.get_cars_arrival_count()), cells))

def get_max_arrival_freq(cells):
    return max(map((lambda c: c.get_cars_arrival_frequency()), cells))

def get_min_arrival_freq(cells):
    return min(map((lambda c: c.get_cars_arrival_frequency()), cells))

def get_avg_arrival_freq(cells):
    return sum(map((lambda c: c.get_cars_arrival_frequency()), cells)) / len(cells)


def get_max_departure_count(cells):
    return max(map((lambda c: c.get_cars_departures_count()), cells))

def get_max_inside_count(cells):
    return max(map((lambda c: c.get_max_cars_inside_count()), cells))

def get_sum_arrival_count(cells):
    return sum(map((lambda c: c.get_cars_arrival_count()), cells))

def get_min_arrival_count(cells):
    return min(map((lambda c: c.get_cars_departures_count()), cells))

