import numpy as np
from glob import glob
import os, sys
import cv2
from PIL import Image

assert len(sys.argv) > 1

def convert_yuv(h, w, msg,convertname):
    img_y=np.frombuffer(msg[:h*w],dtype='uint8').reshape((h,w)).astype('int32')
    img_u=np.frombuffer(msg[h*w+1:h*w+h*w//2:2],dtype='uint8').reshape((h//2,w//2)).astype('int32')
    img_v=np.frombuffer(msg[h*w:h*w+h*w//2:2],dtype='uint8').reshape((h//2,w//2)).astype('int32')
    ruv=((359*(img_v-128))>>8)
    guv=-1*((88*(img_u-128)+183*(img_v-128))>>8)
    buv=((454*(img_u-128))>>8)
    ruv=np.repeat(np.repeat(ruv,2,axis=0),2,axis=1)
    guv=np.repeat(np.repeat(guv,2,axis=0),2,axis=1)
    buv=np.repeat(np.repeat(buv,2,axis=0),2,axis=1)
    img_r=(img_y+ruv).clip(0,255).astype('uint8')
    img_g=(img_y+guv).clip(0,255).astype('uint8')
    img_b=(img_y+buv).clip(0,255).astype('uint8')
    img=np.dstack([img_b[:,:,None],img_g[:,:,None],img_r[:,:,None]])

    img=img.transpose((1,0,2))[::-1].copy()

    saveimg = np.dstack([img_r[:, :, None], img_g[:, :, None], img_b[:, :, None]])

    saveimg = saveimg.transpose((1, 0, 2))[::-1].copy()
    im = Image.fromarray(saveimg)
    im.save(convertname)
    return img
os.system('rm transfer/*')
for path in glob(os.path.join(sys.argv[1], '*.yuv')):
    with open(path, 'rb') as file:
        data = file.read()
        convertname = 'transfer/'+file.name.replace('yuv','png').replace('resource/','')
        print(convertname)
    height = 1080
    width = 1472
    img = convert_yuv(height, width, data,convertname)
    print(img.shape)
    cv2.imshow('image', img)
    key = cv2.waitKey() & 0xff
    if key == ord('q'):
        exit()
