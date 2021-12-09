import itertools
from typing import List
import json

from src.v2x.models import BoundaryBox, Position2d, eNodeB
from src.helpers.map_helpers import project_coords, create_boundary, create_boundary_line_end_points, get_distance, \
    find_lines_crossing, is_in_bbox
from src.helpers.sumo_helpers import extract_projection_details_from_net_file


def extract_eNodeBs_and_create_ranges(sumo_net_file: str, eNodeB_mec_conf_file: str) -> List[eNodeB]:
    """
    1. Reads SUMO net file (network definition) to find network (0,0) point coordinates.
    2. Reads eNodeBs spatial coordinates from file.
    3. Projects eNodeBs coordinates and shifts it based on SUMO net (0,0) point coordinates.
    4. Assign each eNodeB a radial range - boundary points

    Args:
        sumo_net_file (str): net.xml SUMO network definition file
        eNodeB_mec_conf_file: file with longitudes and latitudes of LTE/5G base stations

    Returns:
        List[eNodeB]: list od eNodeBs ready to use, with shifted coordinates
    """
    
    net_offset, conv_bbox, orig_bbox, proj_params = extract_projection_details_from_net_file(sumo_net_file)
    eNodeBs = read_eNodeBs_from_file(eNodeB_mec_conf_file)
    project_and_add_net_offset_for_eNodeBs(eNodeBs, net_offset, proj_params)
    assign_boundaries_efficient(eNodeBs, conv_bbox)

    return eNodeBs


def read_eNodeBs_from_file(eNodeB_mec_conf_file: str) -> List[eNodeB]:
    """Reads eNodeB_MEC configuration file and returns list of eNodeB objects. XYs are spatial coordinates.

    Args:
        eNodeB_mec_conf_file (str): eNodeB-MEC configuration filepath

    Returns:
        List[eNodeB]: list of eNodeB objects with spatial coordinates
    """
    with open(eNodeB_mec_conf_file, 'r') as f:
        eNB_list = json.load(f)
        
    eNodeBs = []
    for eNB_raw in eNB_list:
        # TODO: data validation
        
        eNB = eNodeB(eNB_raw['eNB_id'], eNB_raw['longitude'], eNB_raw['latitude'], eNB_raw['mec_id'])
        eNodeBs.append(eNB)
    
    return eNodeBs


def project_and_add_net_offset_for_eNodeBs(eNodeBs: List[eNodeB], net_offset: List[float], proj_params: dict):
    for eNB in eNodeBs:
        x, y = project_coords(eNB.location.x, eNB.location.y, proj_params)
        x += net_offset[0]
        y += net_offset[1]
        eNB.location = Position2d(x, y)


def assign_boundaries_naive(eNodeBs: List[eNodeB], map_boundary_box: List[float]):
    """
    1. Create grid of points in map area

    Args:
        eNodeBs (List[eNodeB]): [description]
    """
    map_bbox = BoundaryBox(map_boundary_box)


def assign_boundaries_efficient(eNodeBs: List[eNodeB], map_boundary_box: BoundaryBox):
    lines = []
    for enb1, enb2 in itertools.combinations(eNodeBs, 2):
        boundary_line_vertexes = create_boundary_line_end_points(enb1.location, enb2.location, map_boundary_box)
        lines.append(boundary_line_vertexes)

    lines.extend(map_boundary_box.get_lines())

    for line1, line2 in itertools.combinations(lines, 2):
        cross_point = find_lines_crossing(line1, line2)
        if is_in_bbox(cross_point, map_boundary_box):
            distances_to_eNodeBs = map(lambda enb: {'eNB': enb, 'distance': get_distance(cross_point, enb.location)},
                                       eNodeBs)
            sorted_distances = sorted(distances_to_eNodeBs, key=lambda d: d['distance'])

            # First two distances should be equal because the line represents points of equidistant for (at least)
            # two points
            acceptable_diff = 1  # meters
            diff = 0
            for i in range(1, len(sorted_distances)):
                if sorted_distances[i]['distance'] - sorted_distances[0]['distance'] < acceptable_diff:
                    enb = sorted_distances[i]['enb']
                    enb.boundary_points.append(cross_point)
