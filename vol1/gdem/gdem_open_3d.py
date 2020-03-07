import numpy as np
from osgeo import gdal, gdalconst, gdal_array
import matplotlib.pyplot as plt
import matplotlib
from mpl_toolkits.mplot3d import Axes3D

dem_tif = gdal.Open('./ASTGTMV003_N35E139_dem.tif', gdalconst.GA_ReadOnly)
dem = dem_tif.GetRasterBand(1).ReadAsArray()

transform = dem_tif.GetGeoTransform()
x = np.array([transform[0] + i*transform[1] for i in range(dem_tif.RasterXSize)])
y = np.array([transform[3] + i*transform[5] for i in range(dem_tif.RasterYSize)])
X, Y = np.meshgrid(x, y)
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.view_init(elev=30, azim=-80)
surf = ax.plot_surface(X, Y, dem, cmap='gist_gray_r')
plt.show()