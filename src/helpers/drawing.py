from typing import List

import numpy as np
from matplotlib import pyplot as plt
from matplotlib.patches import Polygon as Poly

from src.sumo.net_file_parse import extract_projection_details_from_net_file
from src.v2x.enodeb import read_eNodeBs_from_config, project_and_add_net_offset_for_eNodeBs, assign_boundaries
from src.v2x.mec import extract_mecs_with_ranges


def show_mec_boundaries():
    enbs, bbox = get_enbs_bbox()
    mecs = extract_mecs_with_ranges(enbs)

    bbox_points = list(map(lambda p: (p.x, p.y), bbox.get_all_vertices()))
    bbox_poly = Poly(bbox_points, fill=False)

    colors = []
    [colors.append(np.random.rand(3, )) for _ in range(len(enbs))]

    fig, ax = plt.subplots()

    for index, enb in enumerate(enbs):
        poly = Poly(enb.boundary_points, fill=True, color=colors[index])
        ax.add_patch(poly)

        ax.plot(enb.location.x, enb.location.y, 'o', label=enb.Id, color=colors[index], markeredgecolor='black')

    ax.add_patch(bbox_poly)

    for mec in mecs:
        mec_poly = Poly(mec.boundary_points, fill=False, edgecolor='black')
        ax.add_patch(mec_poly)

    plt.axis('scaled')
    plt.legend()
    plt.show()

def show_enb_boundaries():
    enbs, bbox = get_enbs_bbox()
    bbox_points = list(map(lambda p: (p.x, p.y), bbox.get_all_vertices()))
    bbox_poly = Poly(bbox_points, fill=False)

    colors = []
    [colors.append(np.random.rand(3,)) for _ in range(len(enbs))]

    fig, ax = plt.subplots()

    for index, enb in enumerate(enbs):
        poly = Poly(enb.boundary_points, fill=True, color=colors[index])
        ax.add_patch(poly)

        ax.plot(enb.location.x, enb.location.y, 'o', label=enb.Id, color=colors[index], markeredgecolor='black')

    ax.add_patch(bbox_poly)
    plt.axis('scaled')
    plt.legend()
    plt.show()


def get_enbs_bbox():
    sumo_net_file = '/home/chris/Documents/STUDIA/Praca_mgr/Symulacje/v2x-mec/sumo/net_s8/osm.net.xml'
    eNodeB_mec_conf_file = '/home/chris/Documents/STUDIA/Praca_mgr/Symulacje/v2x-mec/bts/bts-mec-conf.json'

    net_offset, conv_bbox, orig_bbox, proj_params = extract_projection_details_from_net_file(sumo_net_file)
    eNodeBs = read_eNodeBs_from_config(eNodeB_mec_conf_file)
    project_and_add_net_offset_for_eNodeBs(eNodeBs, net_offset, proj_params)
    assign_boundaries(eNodeBs, conv_bbox)

    return eNodeBs, conv_bbox


def show_polygon(points: List):

    poly = Poly(points, fill=True)
    fig, ax = plt.subplots()
    ax.add_patch(poly)

    min_x = min(map(lambda p: p[0], points))
    max_x = max(map(lambda p: p[0], points))
    min_y = min(map(lambda p: p[1], points))
    max_y = max(map(lambda p: p[1], points))

    plt.xlim(min_x - abs(0.1 * min_x), max_x + abs(0.1 * max_x))  # +/- 10%
    plt.ylim(min_y - abs(0.1 * min_y), max_y + abs(0.1 * max_y))
    plt.show()


def show_polygons(polygons: List):
    fig, ax = plt.subplots()
    for polygon in polygons:
        poly = Poly(np.array(polygon), fill=False)
        ax.add_patch(poly)

    plt.show()
