import numpy as np
from PIL import Image

dataset_name = 'A1AVM19970414D064288P1395P360_200UCG6004'

tif_b = Image.open('./{}.band1.tif'.format(dataset_name))
tif_g = Image.open('./{}.band2.tif'.format(dataset_name))
tif_r = Image.open('./{}.band3.tif'.format(dataset_name))

(w, h) = tif_b.size
rgb_array = np.zeros((h, w, 3), dtype = 'uint8')

rgb_array[:,:,0] = tif_r
rgb_array[:,:,1] = tif_g
rgb_array[:,:,2] = tif_b

img = Image.fromarray(rgb_array)
img.save('{}.tif'.format(dataset_name), 'TIFF')
print('created color image.')