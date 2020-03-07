# https://wiki.openstreetmap.org/wiki/Slippy_map_tilenames#Python
import math
def num2deg(xtile, ytile, zoom):
  n = 2.0 ** zoom
  lon_deg = xtile / n * 360.0 - 180.0
  lat_rad = math.atan(math.sinh(math.pi * (1 - 2 * ytile / n)))
  lat_deg = math.degrees(lat_rad)
  return (lat_deg, lon_deg)

print('num2deg')
print('左上: {}'.format(num2deg(1819, 806, 11))) 
print('右上: {}'.format(num2deg(1820, 806, 11))) 
print('左下: {}'.format(num2deg(1819, 807, 11))) 
print('右下: {}'.format(num2deg(1820, 807, 11))) 


def pixel2deg(tile_x, tile_y, zoom, m, n):
    pixel_x = int(tile_x * 2**8) + n
    pixel_y = int(tile_y * 2**8) + m
    pixel_z = zoom + 8
    return num2deg(pixel_x, pixel_y, pixel_z)


print('pixel2deg')
print('左上: {}'.format(pixel2deg(1819, 806, 11, 0, 0))) 
print('右上: {}'.format(pixel2deg(1819, 806, 11, 0, 256))) 
print('左下: {}'.format(pixel2deg(1819, 806, 11, 256, 0))) 
print('右下: {}'.format(pixel2deg(1819, 806, 11, 256, 256))) 
print('中央: {}'.format(pixel2deg(1819, 806, 11, 127, 127))) 
