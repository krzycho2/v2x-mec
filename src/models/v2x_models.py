from typing import List
from shapely.geometry import Polygon

from src.models.map_time_models import Position2d


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


class Uct:
    time: float
    dest_mec_id: int

    def __init__(self, time: float = None, dest_mec_id: int = None):
        if time:
            self.time = time

        if dest_mec_id:
            self.dest_mec_id = dest_mec_id


class UctStats:
    max_uct_freq: float
    min_uct_freq: float
    all_uct_count: int

    def __init__(self, max_uct_freq: float = None, min_uct_freq: float = None, all_uct_count: int = None):
        self.max_uct_freq = max_uct_freq
        self.min_uct_freq = min_uct_freq
        self.all_uct_count = all_uct_count


class Mec:
    Id: int
    boundary_points: List[Position2d]
    included_eNodeBs: List[int]
    ucts: List[Uct]

    def __init__(self, mec_id: int) -> None:
        self.Id = mec_id
        self.boundary_points = []
        self.included_eNodeBs = []
        self.ucts = []

    # def include_eNodeB(self, enb: eNodeB):
    #     "Incorporates eNodeB range to Mec boundary_points range."
    #
    #     if not self.boundary_points:
    #         self.boundary_points = enb.boundary_points
    #         self.included_eNodeBs.append(enb.Id)
    #         return
    #
    #     current_boundary_polygon = Polygon(self.boundary_points)
    #
    #     enb_boundary_polygon = Polygon(enb.boundary_points)
    #     current_boundary_polygon.union(enb_boundary_polygon)
    #
    #     self.boundary_points = list(current_boundary_polygon.boundary.coords)
    #
    #     if self.boundary_points[0] == self.boundary_points[-1]:
    #         _ = self.boundary_points.pop()
    #
    #     self.included_eNodeBs.append(enb.Id)