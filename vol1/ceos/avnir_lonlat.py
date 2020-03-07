import re
import math
import numpy as np

with open('./A1AVM19970414D064288P1395P360_200UCG6004/A1AVM19970414D064288P1395P360_200UCG6004.02',mode='rb') as fp:
    head = 4680 * 2

    fp.seek(head + 508,0)
    pixel_number = int(float(fp.read(16)))
    fp.seek(head + 524,0)
    line_number = int(float(fp.read(16)))

    fp.seek(head + 956,0)
    raw_lat_factors = re.findall('((\+|-).+?D(\+|-)\d{3})', fp.read(144).decode())

    fp.seek(head + 1100,0)
    raw_lon_factors = re.findall('((\+|-).+?D(\+|-)\d{3})', fp.read(144).decode())
    
    lat_factors = []
    for raw_factor in raw_lat_factors:
        raw_factor = raw_factor[0].split('D')
        mantissa = float(re.sub('^\+', '', raw_factor[0]))
        exponent = int(re.sub('^\+', '', raw_factor[1]))
        lat_factors.append(mantissa * math.pow(10,exponent))
        
    lon_factors = []
    for raw_factor in raw_lon_factors:
        raw_factor = raw_factor[0].split('D')
        mantissa = float(re.sub('^\+', '', raw_factor[0]))
        exponent = int(re.sub('^\+', '', raw_factor[1]))
        lon_factors.append(mantissa * math.pow(10,exponent))

    lon = np.zeros((line_number, pixel_number))
    lat = np.zeros((line_number, pixel_number))

    for i in range(line_number):
        I = i + 1
        for j in range(pixel_number):
            J = j + 1
            lat[i, j] = lat_factors[0] + lat_factors[1]*I + lat_factors[2]*J  + lat_factors[3]*I*J + lat_factors[4]*I**2 + lat_factors[5]*J**2
            lon[i, j] = lon_factors[0] + lon_factors[1]*I + lon_factors[2]*J  + lon_factors[3]*I*J + lon_factors[4]*I**2 + lon_factors[5]*J**2
            
            
    print(lon[:10, :10])
    print(lat[:10, :10])