from netCDF4 import Dataset
import matplotlib.pyplot as plt
import numpy as np

meteo_file = 'F:\\GIS_DATA\\weather\\2019030600_003.nc'
fh = Dataset(meteo_file, mode='r')

tmax = fh.variables['TMAX_2maboveground'][:]
data = np.mat(tmax[::-1])
plt.xticks([]), plt.yticks([])
plt.imshow(data)
plt.colorbar(shrink=.92)
plt.show()
