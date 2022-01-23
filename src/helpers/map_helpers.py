from pyproj import Proj


def project_coords(longitude: float, latitude: float, proj_params: dict):
    p = Proj(proj=proj_params['proj'], zone=proj_params['zone'], ellps=proj_params['ellps'], preserve_units=False)
    return p(longitude, latitude)
