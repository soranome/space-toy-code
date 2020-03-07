import numpy as np
from PIL import Image
import struct

def get_image_array(file_path):   
    with open(file_path, mode='rb') as fp:
        fp.seek(44,0) 
        try:
            file_number = int(fp.read(4))
            if((file_number + 1) % 3 != 0):
                raise Exception()
        except:
            raise ValueError('This file isn\'t image file.')
        
        fp.seek(186,0)
        image_record_length = int(fp.read(6))
        fp.seek(228,0)
        if fp.read(4).decode('utf-8') == 'RJLR':
        	endian = '>'
        else:
        	endian = '<'

        fp.seek(236,0)
        line_number = int(fp.read(8))
        fp.seek(244,0)
        invalid_left_pixel = int(fp.read(4))
        pixel_number = int(fp.read(8))
        invalid_right_pixel = int(fp.read(4))
        fp.seek(280,0)
        record_header_length = int(fp.read(4))

        arr = np.zeros((line_number, pixel_number), dtype = 'uint8')

        for i in range(line_number):
            head = image_record_length * (i+1)
            fp.seek(head + record_header_length + invalid_left_pixel, 0)
            data = struct.unpack(endian + 'b'*pixel_number, fp.read(pixel_number))
            arr[i, :] = np.array(data)
        return arr

dataset_name = 'A1AVM19970414D064288P1395P360_200UCG6004'
for i in range(4):
    src_name = '{}.{}'.format(dataset_name, str((i + 1)*3).zfill(2))
    src_path = './{}/{}'.format(dataset_name, src_name)

    data = get_image_array(src_path)
    img = Image.fromarray(data)
    img.save('{}.band{}.tif'.format(dataset_name, str(i + 1)), 'TIFF')
    print('created band{}.tif'.format(str(i + 1)))