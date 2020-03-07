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

def pixel2deg(tile_x, tile_y, zoom, n, m):
    pixel_x = int(tile_x * 2**8) + m
    pixel_y = int(tile_y * 2**8) + n
    pixel_z = zoom + 8
    return num2deg(pixel_x, pixel_y, pixel_z)

def get_dem_index(lon, lat, geotif):
    gdem_diff = geotif.GetGeoTransform()[1]
    gdem_left = geotif.GetGeoTransform()[0]
    x = int((lon - gdem_left)/gdem_diff + 0.5)

    gdem_diff = geotif.GetGeoTransform()[5]
    gdem_top = geotif.GetGeoTransform()[3]
    y = int((lat - gdem_top)/gdem_diff + 0.5)
    
    if y < 0 or y >= dem_tif.RasterYSize or x < 0 or x >= dem_tif.RasterXSize:
         raise ValueError('out of range.')
    return (y, x)


def calc_dem_color(dem_value, u=1):
    v = int(dem_value/u)
    b = format(dem_value, 'b').zfill(24)
    r = int(b[:8], 2)
    g = int(b[8:16], 2)
    b = int(b[16:], 2)
    return [r, g, b]

z=11
dem_tif = gdal.Open('./ASTGTMV003_N35E139_dem.tif', gdalconst.GA_ReadOnly)
dem = dem_tif.GetRasterBand(1).ReadAsArray()

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

        for i in range(256):
            for j in range(256):
                (lat, lon) = pixel2deg(x, y, z, i, j)
                try:
                    dem_ij = get_dem_index(lon, lat, dem_tif)
                    value = dem[dem_ij[0],dem_ij[1]]
                except ValueError as e:
                    value = -9999
                if value < 0:
                    tile[i,j, :] = np.array([128, 0, 0])
                else:
                    tile[i,j, :] = np.array(calc_dem_color(value))
                


        img = Image.fromarray(tile)
        img.save('{}/{}.png'.format(dir_path, y))