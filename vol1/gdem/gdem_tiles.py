import numpy as np
import math
import os
from osgeo import gdal, gdalconst, gdal_array
from PIL import Image

def deg2num(lat_deg, lon_deg, zoom):
    lat_rad = math.radians(lat_deg)
    n = 2.0 ** zoom
    xtile = int((lon_deg + 180.0) / 360.0 * n)
    ytile = int((1.0 - math.asinh(math.tan(lat_rad)) / math.pi) / 2.0 * n)
    return (xtile, ytile)

def num2deg(xtile, ytile, zoom):
    n = 2.0 ** zoom
    lon_deg = xtile / n * 360.0 - 180.0
    lat_rad = math.atan(math.sinh(math.pi * (1 - 2 * ytile / n)))
    lat_deg = math.degrees(lat_rad)
    return (lat_deg, lon_deg)

base_z=11
for z in reversed(range(0, base_z)):
    dem_tif = gdal.Open('./ASTGTMV003_N35E139_dem.tif', gdalconst.GA_ReadOnly)
    transform = dem_tif.GetGeoTransform()
    (lat_size, lon_size) = (dem_tif.RasterYSize, dem_tif.RasterXSize)
    lon_diff = transform[1]
    lat_diff = transform[5]
    lt = [transform[0], transform[3]]
    rb = [transform[0] + lon_diff * lon_size, transform[3] + lat_diff * lat_size]


    lt_xy = deg2num(lt[1], lt[0], z)
    rb_xy = deg2num(rb[1], rb[0], z)

    for x in range(lt_xy[0], rb_xy[0]+1):
        dir_path = './{}/{}'.format(z, x)
        os.makedirs(dir_path, exist_ok=True)
        for y in range(lt_xy[1], rb_xy[1]+1):
            tile = np.zeros((256, 256, 3), np.uint8)
            for xx in range(2):
                for yy in range(2):
                    try:
                        parent_tile = np.asarray(Image.open('./{}/{}/{}.png'.format(z+1, 2*x + xx, 2*y + yy)))
                        tile[128*yy:128*(yy+1), 128*xx:128*(xx+1), :] = parent_tile[:-1:2,:-1:2,:]
                    except:
                        pass

            img = Image.fromarray(tile)
            img.save('./{}/{}.png'.format(dir_path, y))


