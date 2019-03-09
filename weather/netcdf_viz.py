from netCDF4 import Dataset
import matplotlib.pyplot as plt
import numpy as np

nc_file = 'F:\\GIS_DATA\\weather\\2019030600_003.nc'
ds = Dataset(nc_file, mode='r')

tmax = ds.variables['TMAX_2maboveground'][:]
data = np.mat(tmax[::-1])
plt.xticks([]), plt.yticks([])
plt.imshow(data)
plt.colorbar(shrink=.92)
plt.show()
ds.close()
