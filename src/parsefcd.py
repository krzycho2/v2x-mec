
"""
This the main script
"""
from src.v2x.enodeb import extract_eNodeBs_and_create_ranges
from src.v2x.cars import extract_car_time_locations_from_fcd_file
from src.v2x.mec import extract_mecs_with_ranges
from src.v2x.uct import calculate_and_print_uct_stats


def read_sumo_files_and_calculate_uct_stats(fcd_file: str, net_file: str, eNodeBs_mec_config_file: str):
    
    car_time_locations = extract_car_time_locations_from_fcd_file(fcd_file)
    
    eNodeBs = extract_eNodeBs_and_create_ranges(net_file, eNodeBs_mec_config_file)
    
    mecs = extract_mecs_with_ranges(eNodeBs)
    
    calculate_and_print_uct_stats(car_time_locations, mecs)


# for test purposes
net_file = '/home/chris/Documents/STUDIA/Praca_mgr/Symulacje/v2x-mec/sumo/net_s8/osm.net.xml'
fcd_file = '/home/chris/Documents/STUDIA/Praca_mgr/Symulacje/v2x-mec/sumo/outputs/net_s8.xml'
eNodeB_mec_config = '/home/chris/Documents/STUDIA/Praca_mgr/Symulacje/v2x-mec/bts/bts-mec-conf.json'
read_sumo_files_and_calculate_uct_stats(fcd_file, net_file, eNodeB_mec_config)
