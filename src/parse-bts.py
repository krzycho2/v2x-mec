from helpers.drawing import draw_eNodeBs_map
from maphelpers import  assign_eNodeBs_to_map_squares, create_map_squares, read_eNodeBs_from_file


BTS_COORDS_FILE_PATH = '../bts/bts-coords.txt'
# MAP_BOUNDARY_FILE_PATH = '/home/chris/Documents/STUDIA/Praca_mgr/Symulacje/v2x-mec/bts/square-tops.txt'
MAP_BBOX_JSON_FILE = '../bts/map-bbox.json'

# main
def create_bts_boundaries() -> list:
    
    """
    1. Projekcja współrzędnych btsów i mapy
    1. Podzielić mapę na siatkę 50x50 (2500 kwadratów) i uzyskać jego współrzędne
    2. Dla każdego z kwadratu obliczyć odległość od każdego z btsów
    """
    
    pass

eNBs = read_eNodeBs_from_file(BTS_COORDS_FILE_PATH)
map_squares = create_map_squares(MAP_BBOX_JSON_FILE)
assign_eNodeBs_to_map_squares(eNBs, map_squares)
print('elo')


draw_eNodeBs_map(eNBs, map_squares)