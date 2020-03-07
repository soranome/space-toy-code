from osgeo import gdal, gdalconst, gdal_array

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


dem_tif = gdal.Open('./ASTGTMV003_N35E139_dem.tif', gdalconst.GA_ReadOnly)
dem = dem_tif.GetRasterBand(1).ReadAsArray()

# 画像内の座標
try:
    lon = 139.5
    lat = 35.8
    dem_ij = get_dem_index(lon, lat, dem_tif)
    print('({}, {})=> i:{}, j:{}, {}[m]'.format(lon, lat, dem_ij[0],dem_ij[1], dem[dem_ij[0],dem_ij[1]]))
except ValueError as e:
    print(e)

# 左下座標
try:
    lon = dem_tif.GetGeoTransform()[0]
    lat = dem_tif.GetGeoTransform()[3] + dem_tif.GetGeoTransform()[5] * (dem_tif.RasterYSize - 1)
    dem_ij = get_dem_index(lon, lat, dem_tif)
    print('({}, {})=> i:{}, j:{}, {}[m]'.format(lon, lat, dem_ij[0],dem_ij[1], dem[dem_ij[0],dem_ij[1]]))
except ValueError as e:
    print(e)

# 右下座標
try:
    lon = dem_tif.GetGeoTransform()[0] + dem_tif.GetGeoTransform()[1] * (dem_tif.RasterXSize - 1)
    lat = dem_tif.GetGeoTransform()[3] + dem_tif.GetGeoTransform()[5] * (dem_tif.RasterYSize - 1)
    dem_ij = get_dem_index(lon, lat, dem_tif)
    print('({}, {})=> i:{}, j:{}, {}[m]'.format(lon, lat, dem_ij[0],dem_ij[1], dem[dem_ij[0],dem_ij[1]]))
except ValueError as e:
    print(e)
    
# 範囲外の座標
try:
    lon = 180
    lat = 83.5
    dem_ij = get_dem_index(lon, lat, dem_tif)
    print('({}, {})=> i:{}, j:{}, {}[m]'.format(lon, lat, dem_ij[0],dem_ij[1], dem[dem_ij[0],dem_ij[1]]))
except ValueError as e:
    print('({}, {})=> {}'.format(lon, lat, e))
    
