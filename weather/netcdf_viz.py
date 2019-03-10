from netCDF4 import Dataset
import matplotlib.pyplot as plt
import numpy as np

nc_file = 'F:\\GIS_DATA\\weather\\2019030600_003.nc'
ds = Dataset(nc_file, mode='r')

tmax = ds.variables['TMAX_2maboveground'][:]
data = np.mat(tmax[::-1])

plt.figure(figsize=(14, 12), dpi=100)
plt.gca().xaxis.set_major_locator(plt.NullLocator())
plt.gca().yaxis.set_major_locator(plt.NullLocator())
plt.subplots_adjust(top=1, bottom=0, right=1, left=0, hspace=0, wspace=0)
plt.margins(0, 0)

#plt.xticks([]), plt.yticks([])
plt.imshow(data, aspect='equal')
# plt.colorbar(shrink=.92)
plt.savefig('2019030600_003.png', format='png', transparent=True, pad_inches=0)
plt.show()
ds.close()
