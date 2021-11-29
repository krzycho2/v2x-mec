from typing import List

from models import eNodeB



def extract_eNodeBs_and_create_ranges(sumo_net_file: str, eNodeBs_locations_file: str) -> List[eNodeB]:
    """
    1. Reads SUMO net file (network definition) to find network (0,0) point coordinates.
    2. Reads eNodeBs spatial coordinates from file.
    3. Projects eNodeBs coordinates and shifts it based on SUMO net (0,0) point coordinates.

    Args:
        sumo_net_file (str): net.xml SUMO network definition file
        eNodeBs_locations_file: file with longitudes and latitudes of LTE/5G base stations

    Returns:
        List[eNodeB]: list od eNodeBs ready to use, with shifted coordinates
    """
    
    # TODO
    pass