from typing import List
from shapely.geometry import Polygon
from shapely.ops import unary_union

from src.models.v2x_models import eNodeB, Mec


def extract_mecs_with_ranges(eNodeBs: List[eNodeB]) -> List[Mec]:
    """Extract MECs from eNodeBs and creates boundary points (range) for each MEC.

    Args:
        eNodeBs (List[eNodeB]): All eNodeBs

    Returns:
        List[Mec]: List of created MECs.
    """
    mecs: List[Mec] = []
    [mecs.append(Mec(mec_id)) for mec_id in set(map(lambda enb: enb.assigned_mec_id, eNodeBs))]

    for mec in mecs:
        mec_eNodeBs = list(filter(lambda enb: enb.assigned_mec_id == mec.Id, eNodeBs))
        polygons = list(map(lambda enb: Polygon(enb.boundary_points), mec_eNodeBs))
        mec.included_eNodeBs = list(map(lambda enb: enb.Id, mec_eNodeBs))

        merged_polygon = unary_union(polygons)

        if type(merged_polygon) != Polygon:
            raise ValueError('eNodeBs assigned for MEC dont adhere! Closing...')

        mec.boundary_points = list(merged_polygon.boundary.coords)

        if mec.boundary_points[0] == mec.boundary_points[-1]:
            _ = mec.boundary_points.pop()

    return mecs
