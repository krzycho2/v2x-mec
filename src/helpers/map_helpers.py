from math import radians, cos, sin, asin, sqrt, ceil

from typing import List

from pyproj import Proj
import xmltodict
from ..v2x.models import BoundaryBox, Position2d

POINT_GRID_DELTA = Position2d(10, 10)


def get_distance(point1: Position2d, point2: Position2d) -> float:
    return sqrt((point1.x - point2.x) ** 2 + (point1.y - point2.y) ** 2)


def project_coords(longitude: float, latitude: float, proj_params: dict):

    p = Proj(proj=proj_params['proj'], zone=proj_params['zone'], ellps=proj_params['ellps'], preserve_units=False)
    return p(longitude, latitude)


def is_point_in_area(point: Position2d, area_boundary_points: List[Position2d]) -> bool:
    """Checks if the provided point is inside area created by area_boundary_points.

    Args:
        point (Point)
        area_boundary_points (List[Point]): List of points that creates area
    """
    # TODO
    pass


def create_boundary(point1: Position2d, point2: Position2d, bbox: BoundaryBox) -> List[Position2d]:
    """
    Summary:
        Creates boundary (list of points) where point1 and point2 are equally distant.
        Boundary is bounded by bbox (BoundaryBox).
        Boundary points are aligned to grid.
    Args:
        point1:
        point2:
        bbox:

    Returns:
        List of boundary points aligned to grid
    """
    delta_x = POINT_GRID_DELTA.x
    points: List[Position2d] = []

    x = bbox.x_min
    while x <= bbox.x_max:
        y = find_equidistant_y(x, point1, point2)
        if bbox.y_min <= y <= bbox.y_max:
            p = align_point_to_grid_within_bbox(Position2d(x, y), bbox)
            points.append(p)

        x += delta_x

    # TODO: Optimization - if derivative(yy) > 0 and y > bbox.y: break
    return points


def create_boundary_line_end_points(point1: Position2d, point2: Position2d, bbox: BoundaryBox) -> List[Position2d]:
    """
    Summary:
        Creates boundary (list of points) where point1 and point2 are equally distant.
        Boundary is bounded by bbox (BoundaryBox).
        Boundary points are aligned to grid.
    Args:
        point1:
        point2:
        bbox:

    Returns:
        2 vertexes of a boundary line
    """
    def find_boundary_line_coefficients(p1: Position2d, p2: Position2d) -> tuple:
        a = (p2.x - p1.x) / (p1.y - p2.y)
        b = ((p1.y + p2.y) / 2) - (a * (p1.x + p2.x) / 2)
        return a, b

    def line_function(a: float, b: float, arg: float, inverse=False) -> float:
        if inverse:
            return (arg - b) / a

        return a * arg + b

    a, b = find_boundary_line_coefficients(point1, point2)
    points: List[Position2d] = []  # must be 2, no other option
    if bbox.y_min <= line_function(a, b, bbox.x_min, False) <= bbox.y_max:
        p = Position2d(bbox.x_min, line_function(a, b, bbox.x_min, False))
        points.append(p)

    if bbox.y_min <= line_function(a, b, bbox.x_max, False) <= bbox.y_max:
        p = Position2d(bbox.x_max, line_function(a, b, bbox.x_max, False))
        points.append(p)

    if bbox.x_min <= line_function(a, b, bbox.y_min, True) <= bbox.x_max:
        p = Position2d(line_function(a, b, bbox.y_min, True), bbox.y_min)
        points.append(p)

    if bbox.x_min <= line_function(a, b, bbox.y_max, True) <= bbox.x_max:
        p = Position2d(line_function(a, b, bbox.y_max, True), bbox.y_max)
        points.append(p)

    assert(len(points) == 2)

    return points


def find_equidistant_y(x: float, p1: Position2d, p2: Position2d) -> float:
    """Finds y for equidistant point from p1 and p2, having x, using simply Pythagoras."""
    # Halway point
    x12 = (p1.x + p2.x) / 2
    y12 = (p1.y + p2.y) / 2

    # Just pythagoras...
    y = ((x12 - x) ** 2 + (p1.x - x12) ** 2 + (p1.y - y12) ** 2 - (p1.x - x) ** 2 - p1.y ** 2 + y12 ** 2) / 2 / (
                y12 - p1.y)
    return y


def align_point_to_grid_within_bbox(point: Position2d, bbox: BoundaryBox = None):

    def align_point_to_grid(point: Position2d):
        x = round(point.x / POINT_GRID_DELTA.x) * POINT_GRID_DELTA.x
        y = round(point.y / POINT_GRID_DELTA.x) * POINT_GRID_DELTA.y
        return Position2d(x, y)

    p = align_point_to_grid(point)
    if p.x > bbox.x_max:
        p.x = round(point.x / POINT_GRID_DELTA.x) * (POINT_GRID_DELTA.x - 1)

    elif p.x < bbox.x_min:
        p.x = round(point.x / POINT_GRID_DELTA.x) * (POINT_GRID_DELTA.x + 1)

    if p.y > bbox.y_max:
        p.y = round(point.x / POINT_GRID_DELTA.x) * (POINT_GRID_DELTA.y - 1)

    elif p.y < bbox.y_min:
        p.y = round(point.x / POINT_GRID_DELTA.x) * (POINT_GRID_DELTA.y + 1)

    return p


def find_lines_crossing(line1: list, line2: list):
    """
    Summary:
        Returns None if lines are parallel.
    Args:
        line1: list of two points on a first line
        line2: list of two points on a second line

    Returns:
        Point (Position2d) of lines crossing or None if lines are parallel
    """

    def find_line_coefficients(p1: Position2d, p2: Position2d) -> tuple:
        a = (p2.y - p1.y) / (p2.x - p1.x)
        b = p1.y - a * p1.x
        return a, b

    a1, b1 = find_line_coefficients(*line1)
    a2, b2 = find_line_coefficients(*line2)

    if a1 == a2:
        return None

    x = (b2 - b1) / (a1 - a2)
    y = a1 * x + b1

    return Position2d(x, y)

def is_in_bbox(point: Position2d, bbox: BoundaryBox) -> bool:
    return bbox.x_min >= point.x >= bbox.x_max and bbox.y_min >= point.y >= bbox.y_max