
"""
This the main script
"""
import logging

from src.constants import DEFAULT_LOGGER_NAME
from src.helpers.time_helpers import print_execution_time
from src.runner import read_config_and_execute_runs
from src.sumo.parse_fcd import load_fcd_data_parallel

logger = logging.getLogger(DEFAULT_LOGGER_NAME)
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
logger.addHandler(ch)


@print_execution_time
def read_sumo_files_and_calculate_uct_stats(fcd_file: str, net_file: str, eNodeB_mec_config_file: str):
    logger.info('Loading fcd data')
    car_time_location_raw = load_fcd_data_parallel(fcd_file)
    read_config_and_execute_runs(car_time_location_raw, net_file, eNodeB_mec_config_file)


# net_file = '/home/chris/Documents/STUDIA/Praca_mgr/Symulacje/v2x-mec/sumo/net_s8/osm.net.xml'
# fcd_file = '/home/chris/Documents/STUDIA/Praca_mgr/Symulacje/v2x-mec/sumo/outputs/net_s8.xml'
# eNodeB_mec_config_file = '/home/chris/Documents/STUDIA/Praca_mgr/Symulacje/v2x-mec/bts/bts-mec-conf.json'

net_file = '/home/chris/s8/osm.net.xml'
fcd_file = '/home/chris/s8/fcd-output.xml'
eNodeB_mec_config_file = '/home/chris/Documents/STUDIA/Praca_mgr/Symulacje/v2x-mec/bts/bts-mec-conf.json'
read_sumo_files_and_calculate_uct_stats(fcd_file, net_file, eNodeB_mec_config_file)
