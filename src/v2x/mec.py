from __future__ import annotations

import logging
from typing import List
from shapely.geometry import Polygon, Point
from shapely.ops import unary_union

from src.constants import DEFAULT_LOGGER_NAME
from src.models.map_time_models import Position2d
from src.models.v2x_models import eNodeB, Mec

logger = logging.getLogger(DEFAULT_LOGGER_NAME)


def extract_mecs_with_ranges(eNodeBs: List[eNodeB]) -> List[Mec]:
    """Extract MECs from eNodeBs and creates boundary points (range) for each MEC.

    Args:
        eNodeBs (List[eNodeB]): All eNodeBs

    Returns:
        List[Mec]: List of created MECs.
    """

    logger.info('Extracting MECs')
    mecs: List[Mec] = []
    [mecs.append(Mec(mec_id)) for mec_id in set(map(lambda enb: enb.assigned_mec_id, eNodeBs))]

    for mec in mecs:
        mec_eNodeBs = list(filter(lambda enb: enb.assigned_mec_id == mec.Id, eNodeBs))

        if len(mec_eNodeBs) == 1:
            mec.boundary_points = mec_eNodeBs[0].boundary_points
            mec.included_eNodeBs = [mec_eNodeBs[0].Id]

        else:
            eNodeBs_boundary_points_polygons = list(map(lambda enb: Polygon(enb.boundary_points), mec_eNodeBs))
            mec.included_eNodeBs = list(map(lambda enb: enb.Id, mec_eNodeBs))

            merged_polygon = unary_union(eNodeBs_boundary_points_polygons)

            if type(merged_polygon) != Polygon:
                logger.error('eNodeBs assigned for MEC dont adhere! Closing...')
                raise ValueError('eNodeBs assigned for MEC dont adhere! Closing...')

            mec.boundary_points = list(merged_polygon.boundary.coords)

            if mec.boundary_points[0] == mec.boundary_points[-1]:
                _ = mec.boundary_points.pop()

    return mecs


def get_mec_by_location(location: Position2d, mecs: List[Mec]) -> Mec | None:

    def mec_contains(mec: Mec, location: Position2d):
        poly = Polygon(mec.boundary_points)
        return poly.contains(Point(location.x, location.y))

    return next(filter(lambda mec: mec_contains(mec, location), mecs), None)


def get_mec_id_by_eNodeB_id(eNodeB_id: int, mecs: List[Mec]):
    return next(filter(lambda mec: eNodeB_id in mec.included_eNodeBs, mecs)).Id
