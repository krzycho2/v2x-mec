from typing import List

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
    time_step: float
    dest_mec_id: int

    def __init__(self, time_step: float, dest_mec_id: int = None):
        if time_step:
            self.time_step = time_step

        if dest_mec_id:
            self.dest_mec_id = dest_mec_id


class Mec:
    Id: int
    boundary_points: List[Position2d]
    included_eNodeBs: List[int]
    # ucts: List[Uct]
    uct_times: List[float]

    def __init__(self, mec_id: int) -> None:
        self.Id = mec_id
        self.boundary_points = []
        self.included_eNodeBs = []
        self.uct_times: List[float] = []


class UctStats:
    run_id: int
    max_uct_freq: float
    min_uct_freq: float
    all_uct_count: int
    mecs_uct_stats: List[dict]

    def __init__(self, max_uct_freq: float = None, min_uct_freq: float = None, all_uct_count: int = None):
        self.max_uct_freq = max_uct_freq
        self.min_uct_freq = min_uct_freq
        self.all_uct_count = all_uct_count

