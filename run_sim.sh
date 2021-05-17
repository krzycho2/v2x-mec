#!/bin/bash
sumo -c net_s8/osm.sumocfg --fcd-output outputs/net_s8.xml --fcd-output.attributes id,x,y \
-b 0 -e 3600 --step-length 0.1 
python3 parse.py outputs/net_s8.xml

# sumo-gui -c net_s8/osm.sumocfg -b 0 -e 3000 --step-length 0.1 