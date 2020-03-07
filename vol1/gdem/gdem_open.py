from osgeo import gdal, gdalconst, gdal_array
import matplotlib.pyplot as plt
import matplotlib
from mpl_toolkits.mplot3d import Axes3D

dem_tif = gdal.Open('./ASTGTMV003_N35E139_dem.tif', gdalconst.GA_ReadOnly)
dem = dem_tif.GetRasterBand(1).ReadAsArray()
transform = dem_tif.GetGeoTransform()
print('始点端経度,東西分解能,回転角,始点端緯度,回転角,南北分解能: {}'.format(transform))

print('tifサイズ: ({},{})'.format(dem_tif.RasterYSize,dem_tif.RasterXSize))

plt.imshow(dem, cmap='gist_gray_r')
plt.show()