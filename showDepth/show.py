import numpy as np
from glob import glob
import os, sys
import cv2
from PIL import Image

assert len(sys.argv) > 1

def convert_yuv(h, w, msg,convertname):
    gray=np.frombuffer(msg[:h*w*2],dtype='uint16').reshape((h,w)).astype('int32')
    gray=gray>>2
    img_b= img_g = img_r=gray.clip(0,255).astype('uint8')
    img=np.dstack([img_b[:,:,None],img_g[:,:,None],img_r[:,:,None]])


    saveimg = np.dstack([img_r[:, :, None], img_g[:, :, None], img_b[:, :, None]])

    saveimg = saveimg.transpose((1, 0, 2))[::-1].copy()
    im = Image.fromarray(saveimg)
    im.save(convertname)
    return img
os.system('rm transfer/*')
for path in glob(os.path.join(sys.argv[1], '*.raw')):
    with open(path, 'rb') as file:
        data = file.read()
        convertname = 'transfer/'+file.name.replace('raw','png').replace('resource/','')
        print(convertname)
    height = 480
    width = 640
    img = convert_yuv(height, width, data,convertname)
    print(img.shape)
    cv2.imshow('image', img)
    key = cv2.waitKey() & 0xff
    if key == ord('q'):
        exit()
