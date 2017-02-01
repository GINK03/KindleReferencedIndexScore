import os

import numpy
from PIL import Image, ImageDraw, ImageFont
import six

import numpy as np

from io import BytesIO
import os
import pickle
import json
import numpy as np

import skimage.io as io

from chainer.dataset import dataset_mixin

# download `BASE` dataset from http://cmp.felk.cvut.cz/~tylecr1/facade/
class FacadeDataset(dataset_mixin.DatasetMixin):
    def __init__(self, dataDir='./facade/base', data_range=(1,300)):
        print("load dataset start")
        print("    from: %s"%dataDir)
        print("    range: [%d, %d)"%(data_range[0], data_range[1]))
        self.dataDir = dataDir
        self.dataset = []
        for i in range(data_range[0],data_range[1]):
            img = Image.open(dataDir+"/cmp_b%04d.jpg"%i)
            label = Image.open(dataDir+"/cmp_b%04d.png"%i)
            w,h = img.size
            r = 286/min(w,h)
            # resize images so that min(w, h) == 286
            img = img.resize((int(r*w), int(r*h)), Image.BILINEAR)
            label = label.resize((int(r*w), int(r*h)), Image.NEAREST)
            
            img = np.asarray(img).astype("f").transpose(2,0,1)/128.0-1.0
            label_ = np.asarray(label)-1  # [0, 12)
            label = np.zeros((12, img.shape[1], img.shape[2])).astype("i")
            for j in range(12):
                label[j,:] = label_==j
            self.dataset.append((img,label))
        print("load dataset done")
    
    def __len__(self):
        return len(self.dataset)

    # return (label, img)
    def get_example(self, i, crop_width=256):
        _,h,w = self.dataset[i][0].shape
        x_l = np.random.randint(0,w-crop_width)
        x_r = x_l+crop_width
        y_l = np.random.randint(0,h-crop_width)
        y_r = y_l+crop_width
        return self.dataset[i][1][:,y_l:y_r,x_l:x_r], self.dataset[i][0][:,y_l:y_r,x_l:x_r]
    
class VecDataset(dataset_mixin.DatasetMixin):
    def __init__(self, dataDir='./base', data_range=(1,100)):
        from glob import glob as glob
        print("load Vec-dataset start")
        print("    from: %s"%dataDir)
        print("    range: [%d, %d)"%(data_range[0], data_range[1]))
        self.IN_CH = 4
        self.dataDir = dataDir
        self.dataset = []
        files = glob('./font-image-gen/fonts/*')
        orgs = list(filter(lambda x:'.org.' in x, files))
        heads = []
        for org in orgs:
            heads.append( org.split('.')[1].split('/').pop() )
            print( org.split('.')[1].split('/').pop() )
        for i in range(data_range[0],data_range[1]):
            head = heads[i]
            """
            headが入っているのが、jsonのキーにもなる
            """
            print(i, "/", data_range[1] - data_range[0], head)

            img_path = list(filter(lambda x: head in x and '.org.' in x, files)).pop()
            lbl_path = list(filter(lambda x: head in x and '.cnv.' in x, files)).pop()
            img = Image.open(img_path)
            label = Image.open(lbl_path).convert('RGB')
            label_org = label
            w,h = img.size
            r = 286/min(w,h)
            # resize images so that min(w, h) == 286
            img = img.resize((int(r*w), int(r*h)), Image.BILINEAR)
            label = label.resize((int(r*w), int(r*h)), Image.NEAREST)
            img = np.asarray(img).astype("f").transpose(2,0,1)/128.0-1.0
            
            lbl_ = np.array(label)  # [0, 12)
            
            to_return = np.zeros((self.IN_CH, lbl_.shape[0], lbl_.shape[1])).astype('uint8')
            to_return[0, :, :] = lbl_[:, :, 0]
            to_return[1, :, :] = lbl_[:, :, 1]
            to_return[2, :, :] = lbl_[:, :, 2]
            #to_return[3, :tagvec.shape[0], :tagvec.shape[1]] = tagvec

            self.dataset.append((img, to_return))

        print("load Vec-dataset done")
    
    def __len__(self):
        return len(self.dataset)

    # return (label, img)
    def get_example(self, i, crop_width=256):
        _,h,w = self.dataset[i][0].shape
        x_l = np.random.randint(0,w-crop_width)
        x_r = x_l+crop_width
        y_l = np.random.randint(0,h-crop_width)
        y_r = y_l+crop_width
        """ cropping する際に、メタ情報もクロッピングしてはならないので、クロッピング範囲を0:2に限定する"""
        cnv = self.dataset[i][1]
        red, grn, blu, meta = cnv[0,y_l:y_r,x_l:x_r], cnv[1,y_l:y_r,x_l:x_r], cnv[2,y_l:y_r,x_l:x_r], \
                cnv[3:,0:256,0:256]
        to_return = np.zeros((self.IN_CH, 256, 256))
        to_return[0, :, :] = red
        to_return[1, :, :] = grn
        to_return[2, :, :] = blu
        to_return[3:, :, :] =  meta
        return to_return, self.dataset[i][0][:,y_l:y_r,x_l:x_r]
        #return self.dataset[i][1][:,y_l:y_r,x_l:x_r], self.dataset[i][0][:,y_l:y_r,x_l:x_r]

if __name__ == '__main__':
    vec = VecDataset( None )
