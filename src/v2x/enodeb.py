from typing import List
import json
import logging

from shapely.geometry import MultiPoint, Point, box, Polygon
from shapely.ops import voronoi_diagram

from src.constants import DEFAULT_CONFIG_CONFIG_KEY, eNB_ID_CONFIG_KEY, eNB_LONGITUDE_CONFIG_KEY, eNB_LATITUDE_CONFIG_KEY, \
    eNB_MEC_ID_CONFIG_KEY, DEFAULT_LOGGER_NAME
from src.helpers.map_helpers import project_coords
from src.models.map_time_models import Position2d, BoundaryBox
from src.models.v2x_models import eNodeB
from src.sumo.net_file_parse import extract_projection_details_from_net_file

logger = logging.getLogger(DEFAULT_LOGGER_NAME)


def extract_eNodeBs_and_create_ranges(sumo_net_file: str, config: dict) -> List[eNodeB]:
    """
    1. Reads SUMO net file (network definition) to find network (0,0) point coordinates.
    2. Reads eNodeBs spatial coordinates from file.
    3. Projects eNodeBs coordinates and shifts it based on SUMO net (0,0) point coordinates.
    4. Assign each eNodeB a radial range - boundary points

    Args:
        sumo_net_file (str): net.xml SUMO network definition file
        config: dict with longitudes and latitudes of LTE/5G base stations

    Returns:
        List[eNodeB]: list od eNodeBs ready to use, with shifted coordinates
    """
    logger.debug('Extracting eNodeBs')

    net_offset, conv_bbox, orig_bbox, proj_params = extract_projection_details_from_net_file(sumo_net_file)
    eNodeBs = read_eNodeBs_from_config_dict(config)
    project_and_add_net_offset_for_eNodeBs(eNodeBs, net_offset, proj_params)
    assign_boundaries(eNodeBs, conv_bbox)

    return eNodeBs


def read_eNodeBs_from_config_dict(config: dict) -> List[eNodeB]:
    eNodeBs: List[eNodeB] = []

    for eNB_raw in config[DEFAULT_CONFIG_CONFIG_KEY]:
        # TODO: data validation

        eNB = eNodeB(id=eNB_raw[eNB_ID_CONFIG_KEY], x=eNB_raw[eNB_LONGITUDE_CONFIG_KEY],
                     y=eNB_raw[eNB_LATITUDE_CONFIG_KEY], assigned_mec_id=eNB_raw[eNB_MEC_ID_CONFIG_KEY])

        eNodeBs.append(eNB)

    return eNodeBs


def read_eNodeBs_from_config_file(eNodeB_mec_conf_file: str) -> List[eNodeB]:
    """Reads eNodeB_MEC configuration file and returns list of eNodeB objects. XYs are spatial coordinates.

    Args:
        eNodeB_mec_conf_file (str): eNodeB-MEC configuration filepath

    Returns:
        List[eNodeB]: list of eNodeB objects with spatial coordinates
    """
    with open(eNodeB_mec_conf_file, 'r') as f:
        eNB_list = json.load(f)

    return read_eNodeBs_from_config_dict(eNB_list)


def project_and_add_net_offset_for_eNodeBs(eNodeBs: List[eNodeB], net_offset: List[float], proj_params: dict):
    for eNB in eNodeBs:
        x, y = project_coords(eNB.location.x, eNB.location.y, proj_params)
        x += net_offset[0]
        y += net_offset[1]
        eNB.location = Position2d(x, y)


def assign_boundaries(eNodeBs: List[eNodeB], map_bbox: BoundaryBox):
    eNodeB_points = list(map(lambda enb: Point(enb.location.x, enb.location.y), eNodeBs))  # cast to shapely Point
    eNodeBs_multi_point = MultiPoint(eNodeB_points)

    polygons = voronoi_diagram(eNodeBs_multi_point)
    bbox_polygon = box(map_bbox.x_min, map_bbox.y_min, map_bbox.x_max, map_bbox.y_max)

    for poly in polygons:
        for enb in eNodeBs:
            enb_point = Point(enb.location.x, enb.location.y)
            if enb_point.within(poly):
                bounded_poly = poly.intersection(bbox_polygon)
                enb.boundary_points = list(bounded_poly.boundary.coords)

                if enb.boundary_points[0] == enb.boundary_points[-1]:
                    _ = enb.boundary_points.pop()

    assert(all(map(lambda enb: len(enb.boundary_points) != 0 or enb.boundary_points is not None, eNodeBs)))


def get_eNodeB_id_by_location(location: Position2d, eNodeBs: List[eNodeB]):

    def enb_contains(enb: eNodeB, location: Position2d):
        poly = Polygon(enb.boundary_points)
        return poly.contains(Point(location.x, location.y))

    enb = next(filter(lambda mec: enb_contains(mec, location), eNodeBs), None)

    if enb is None:
        raise ValueError(f'No eNodeB for location ' + str(location))

    return enb.Id


