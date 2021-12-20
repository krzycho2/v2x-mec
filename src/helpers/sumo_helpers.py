import xmltodict

from src.models.map_time_models import BoundaryBox


def extract_projection_details_from_net_file(sumo_net_file: str) -> tuple:
    """
    Example location line: <location netOffset="-495811.56,-5783648.82" convBoundary="0.00,0.00,7122.86,5710.57" origBoundary="20.938702,52.203274,21.042981,52.254624" projParameter="+proj=utm +zone=34 +ellps=WGS84 +datum=WGS84 +units=m +no_defs"/>

    Args:
        sumo_net_file (str): [description]

    """
    with open(sumo_net_file, 'rb') as f:
        xml_data = xmltodict.parse(f.read())

    location = xml_data['net']['location'] # list
    
    net_offset_raw = location['@netOffset'].split(',')
    net_offset = []
    [net_offset.append(float(x)) for x in net_offset_raw]
    
    conv_boundary_raw = location['@convBoundary'].split(',')
    conv_boundary = []
    [conv_boundary.append(float(x)) for x in conv_boundary_raw]
    conv_bbox = BoundaryBox(*conv_boundary)
    
    orig_boundary_raw = location['@origBoundary'].split(',')
    orig_boundary = []
    [orig_boundary.append(float(x)) for x in orig_boundary_raw]
    orig_bbox = BoundaryBox(*orig_boundary)
    
    proj_parameters_raw = location['@projParameter'].split(' ')
    proj_params = {}
    for proj_param in proj_parameters_raw:
        kv = proj_param.split('=')
        if len(kv) != 2:
            continue
        
        key, value = kv
        key = key[1:]
        if key == 'zone':
            proj_params[key] = int(value)
        
        else:
            proj_params[key] = value
        
    return net_offset, conv_bbox, orig_bbox, proj_params
