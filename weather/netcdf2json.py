import json
import numpy as np
from netCDF4 import Dataset, num2date

np.set_printoptions(precision=1)

nc_file = 'F:\\GIS_DATA\\weather\\2019030600_003.nc'
ds = Dataset(nc_file, mode='r')

nx = ds.dimensions['longitude'].size
ny = ds.dimensions['latitude'].size
# print(num2date(2.019031e+13, 'seconds'))

lons = ds.variables['longitude'][:]
lats = ds.variables['latitude'][:]

u_grid = ds.variables['UGRD_10maboveground'][:]
u_data = np.around(u_grid.flatten(), decimals=1)
v_grid = ds.variables['VGRD_10maboveground'][:]
v_data = np.around(v_grid.flatten(), decimals=1)

u_data[u_data == 9999.0] = 0
v_data[v_data == 9999.0] = 0

print(len(u_grid[0]))


header = {
    'parameterCategory': 2,
    'parameterCategoryName': 'Momentum',
    'parameterNumber': 2,
    'parameterNumberName': 'U-component_of_wind',
    'parameterUnit': 'm.s-1',
    'numberPoints': 1682601,
    'gridUnits': 'degrees',
    'resolution': 48,
    'nx': 1401,
    'ny': 1201,
    'lo1': 70,
    'lo2': 140,
    'la1': 60,
    'la2': 0,
    'dx': 0.05,
    'dy': 0.05
}
u = {
    'header': header.copy(),
    'data': u_data.tolist()
}
v = {
    'header': header.copy(),
    'data': v_data.tolist()
}
v['header']['parameterNumberName'] = 'V_component_of_current'
v['header']['parameterNumber'] = 3

js = {'s': 'you', 'd': 'are', 'd': {'d': 1}}


f = open('gfs1.0.json', 'w')
f.write('[')
f.write(json.dumps(u))
f.write(',')
f.write(json.dumps(v))
f.write(']')

f.close()


