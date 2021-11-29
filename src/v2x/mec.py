from typing import List

from models import Mec, eNodeB



    
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