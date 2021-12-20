
"""
This the main script
"""
from src.v2x.enodeb import extract_eNodeBs_and_create_ranges
from src.v2x.cars import extract_car_time_locations_from_fcd_file
from src.v2x.mec import extract_mecs_with_ranges
from src.v2x.uct import calculate_uct_stats


def read_sumo_files_and_calculate_uct_stats(fcd_file: str, net_file: str):
    
    car_time_locations = extract_car_time_locations_from_fcd_file(fcd_file)
    
    eNodeBs = extract_eNodeBs_and_create_ranges(net_file)
    
    mecs = extract_mecs_with_ranges(eNodeBs)
    
    mec_stats = calculate_uct_stats(car_time_locations, mecs)
    
    print(mec_stats)

# for test purposes

fcd_file = ''
net_file = ''
mec_assignments_file = ''
read_sumo_files_and_calculate_uct_stats(fcd_file, net_file, mec_assignments_file)
