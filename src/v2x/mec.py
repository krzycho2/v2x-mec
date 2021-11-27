from typing import List

from map_time_models import Point
from v2x.enodeb import eNodeB

class Mec:
    Id: int
    boundary_points: List[Point]
    
    def __init__(self, mec_id: int, boundary_points: List[Point]) -> None:
        self.Id = mec_id
        self.boundary_points = boundary_points
        
    def include_eNodeB(self, eNodeB: eNodeB):
        "Incorporates eNodeB range to Mec boundary_points range."
        pass
    
def extract_mecs_with_ranges(eNodeBs: List[eNodeB], mec_assignments_json_file: str) -> List[Mec]:
    """Creates MECs based on mec_assignments and creates boundary points (range) for each MEC.

    Args:
        eNodeBs (List[eNodeB]): All eNodeBs
        mec_assignments_json_file (str): Contains mappings mecId -> list of assigned eNodeBs. Example: [ {mecId: 1, eNodeB_ids: [1,2,3]} ]

    Returns:
        List[Mec]: List of created MECs.
    """
    # TODO
    pass