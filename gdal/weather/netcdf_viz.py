from netCDF4 import Dataset
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import numpy as np

nc_file = r'F:\\GIS_DATA\\weather\\2019030600_003.nc'
ds = Dataset(nc_file, mode='r')

tmax = ds.variables['TMP_2maboveground'][:]
data = np.mat(tmax[::-1])

plt.figure(figsize=(7, 6), dpi=100)
plt.gca().xaxis.set_major_locator(plt.NullLocator())
plt.gca().yaxis.set_major_locator(plt.NullLocator())
plt.subplots_adjust(top=1, bottom=0, right=1, left=0, hspace=0, wspace=0)
plt.margins(0, 0)

#plt.xticks([]), plt.yticks([])
color_dict = [(98, 113, 183,)]

# plt.imshow(data, aspect='equal', vmin=230, vmax=320, cmap=plt.get_cmap('jet'))
plt.imshow(data, aspect='equal', vmin=230, vmax=320, cmap=colors.ListedColormap(color_dict))
# plt.colorbar(shrink=.92)
# plt.savefig('2019030600_003.png', format='png', transparent=True, pad_inches=0)
plt.show()
ds.close()
