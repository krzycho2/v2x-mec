import copyreg
import logging
import multiprocessing as mp
from typing import List
import time
from io import StringIO
from itertools import repeat
import xmltodict
import xml.etree.ElementTree as ET
from lxml import etree
from lxml.etree import XMLParser, parse
from pandas import DataFrame

from src.constants import DEFAULT_LOGGER_NAME
from src.helpers.time_helpers import print_execution_time


def element_unpickler(data):
    return etree.fromstring(data)


def element_pickler(element):
    data = etree.tostring(element)
    return element_unpickler, (data,)


def elementtree_unpickler(data):
    data = StringIO(data)
    return etree.parse(data)


def elementtree_pickler(tree):
    data = StringIO()
    tree.write(data)
    return elementtree_unpickler, (data.getvalue(),)


copyreg.pickle(etree._Element, element_pickler, element_unpickler)
copyreg.pickle(etree._ElementTree, elementtree_pickler, elementtree_unpickler)

logger = logging.getLogger(DEFAULT_LOGGER_NAME)


@print_execution_time
def load_fcd_data_parallel(fcd_file: str) -> List[List]:
    """
    Reads contents of fcd xml file using MultiProcessing library and transforms to list of dicts for each
    car - time - location entry.
    """

    start_time = time.time()
    p = XMLParser(huge_tree=True)
    xml_data = parse(fcd_file, parser=p)
    fcd_data = xml_data.getroot()

    timesteps_count = len(fcd_data.getchildren())
    logger.debug('All timesteps in fcd file: %d', timesteps_count)

    pool = mp.Pool(mp.cpu_count())

    results = pool.map(parse_fcd_timestep2, [timestep for timestep in fcd_data])

    pool.close()
    pool.join()

    flatten_results = [item for sublist in results for item in sublist]
    return flatten_results


def parse_fcd_timestep(timestep) -> List[dict]:
    car_time_location_items: List[dict] = []

    time_stamp = timestep.get('time')

    for raw_car_info in timestep:
        car_id = raw_car_info.get('id')
        pos_x = raw_car_info.get('x')
        pos_y = raw_car_info.get('y')

        car_time_location_items.append({'car_id': car_id, 'time': time_stamp, 'x': pos_x, 'y': pos_y})

    return car_time_location_items


def parse_fcd_timestep2(timestep) -> List[List]:
    time_stamp = timestep.get('time')
    a = [[time_stamp, *raw_car_info.values()] for raw_car_info in timestep]
    return [[time_stamp, *raw_car_info.values()] for raw_car_info in timestep]


@print_execution_time
def load_fcd_data_parallel2(fcd_file):
    xml_data = ET.parse(fcd_file)
    fcd_data = xml_data.getroot()
    pool = mp.Pool(mp.cpu_count())

    car_time_locations = []
    for timestep in fcd_data:
        time_stamp = timestep.get('time')
        car_time_locations.extend(pool.starmap(parse_vehicle, [(vehicle, time_stamp) for vehicle in timestep]))

    return car_time_locations


def parse_vehicle(vehicle, time_stamp):
    return [time_stamp, vehicle.get('id'), vehicle.get('x'), vehicle.get('y')]
