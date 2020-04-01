import json
import numpy as np
from netCDF4 import Dataset

np.set_printoptions(precision=1)

nc_file = 'F:\\GIS_DATA\\weather\\2019030600_003.nc'
ds = Dataset(nc_file, mode='r')

nx = ds.dimensions['longitude'].size
ny = ds.dimensions['latitude'].size

lons = ds.variables['longitude'][:]
lats = ds.variables['latitude'][:]

def vacuate(data):
    d_1 = data[::20]
    for i in range(len(d_1)):
        d_1[i] = d_1[i][::20]
    return np.array(d_1)

u_grid = ds.variables['UGRD_10maboveground'][:]
u_grid_vac = vacuate(u_grid.tolist())
u_data = np.around(u_grid_vac.flatten(), decimals=1).tolist()


v_grid = ds.variables['VGRD_10maboveground'][:]
v_grid_vac = vacuate(v_grid.tolist())
v_data = np.around(v_grid_vac.flatten(), decimals=1).tolist()

u_data[u_data == 9999.0] = None
v_data[v_data == 9999.0] = None


header = {
    'parameterCategory': 2,
    'parameterCategoryName': 'Momentum',
    'parameterNumber': 2,
    'parameterNumberName': 'U-component_of_wind',
    'parameterUnit': 'm.s-1',
    'numberPoints': 4331,
    'gridUnits': 'degrees',
    'resolution': 48,
    'nx': 71,
    'ny': 61,
    'lo1': 70,
    'lo2': 140,
    'la1': 60,
    'la2': 0,
    'dx': 1,
    'dy': 1
}
u = {
    'header': header.copy(),
    'data': u_data
}
v = {
    'header': header.copy(),
    'data': v_data
}
v['header']['parameterNumberName'] = 'V_component_of_current'
v['header']['parameterNumber'] = 3


f = open('current-wind-surface-level-gfs-1.0.json', 'w')
f.write('[')
f.write(json.dumps(u))
f.write(',')
f.write(json.dumps(v))
f.write(']')

f.close()
ds.close()


