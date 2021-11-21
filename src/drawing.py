from typing import List
import matplotlib.pyplot as plt
from maphelpers import MapSquare, eNodeB

def draw_eNodeBs_map(eNodeBs: List[eNodeB], map_MapSquares: List[MapSquare]):
    eNodeBs_xx = list(map(lambda eNB: eNB.x, eNodeBs))
    eNodeBs_yy = list(map(lambda eNB: eNB.y, eNodeBs))
    
    # Print enbs' ranges in different colors
    for eNodeB in eNodeBs:
        MapSquares_for_that_enb = list(filter(lambda s: s.eNodeB.id == eNodeB.id, map_MapSquares))
        MapSquares_center_xx = list(map(lambda MapSquare: MapSquare.center_x, MapSquares_for_that_enb))
        MapSquares_center_yy = list(map(lambda MapSquare: MapSquare.center_y, MapSquares_for_that_enb))
        
        plt.scatter(MapSquares_center_xx, MapSquares_center_yy, marker='.')
        
    # draw eNodeBs
    plt.scatter(eNodeBs_xx, eNodeBs_yy, c='black')
    
    plt.show()
    