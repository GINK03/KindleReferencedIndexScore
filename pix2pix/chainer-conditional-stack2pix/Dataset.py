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

from glob import glob as glob
import json
from chainer.dataset import dataset_mixin

class SixthDataset(dataset_mixin.DatasetMixin):
    def __init__(self, dataDir='./base', data_range=(1,100)):
        print("load Vec-dataset start")
        print("    from: %s"%dataDir)
        print("    range: [%d, %d)"%(data_range[0], data_range[1]))
        self.IN_CH = 4
        self.dataDir = dataDir
        self.dataset = []
        files = glob('./pics.sixth/*')
        orgs = list(filter(lambda x:'.org.' in x, files))
        heads = []
        for org in orgs:
            heads.append( '.'.join(org.split('.')[1:6]).split('/').pop() )
            print(org)
        linker_tags = json.loads(open('./linker_tags_sixth.json').read())
        for i in range(data_range[0],data_range[1]):
            head = heads[i]
            """
            headが入っているのが、jsonのキーにもなる
            """
            print(i, "/", data_range[1] - data_range[0], head)
            tagvec = np.array(linker_tags[head + '.jpg']['vector'])
            """
            meta tag vecを可変にする
            """
            tagvec = np.resize(tagvec, (256,256) )
            tagvec *= 255
            img_path = list(filter(lambda x: head in x and '.org.' in x, files)).pop()
            lbl_path = list(filter(lambda x: head in x and '.cnv.' in x, files)).pop()
            img = Image.open(img_path)
            label = Image.open(lbl_path).convert('RGB')
            label_org = label
            w,h = img.size
            r = 286/min(w,h)
            img = img.resize((int(r*w), int(r*h)), Image.BILINEAR)
            label = label.resize((int(r*w), int(r*h)), Image.NEAREST)
            img = np.asarray(img).astype("f").transpose(2,0,1)/128.0-1.0
            lbl_ = np.array(label)  # [0, 12)
            """
            FIX : このパラメータで、メタ情報領域を生成する
            """
            FIX = 1
            red, grn, blu = lbl_[:,:,0], lbl_[:,:,1], lbl_[:,:,2]
            label = np.zeros((self.IN_CH, img.shape[1], img.shape[2])).astype("i")
            for j, e in [(0, red), (1, grn), (2, blu), (3, tagvec)]:
                if j == 3:
                  print("Enter meta execution")
                  label[j,:tagvec.shape[0], :tagvec.shape[1]] = tagvec
                elif j == 0 or j == 1 or j == 2:
                  label[j,:] = e
            t = np.zeros((label.shape[1], label.shape[2], self.IN_CH -1)).astype('uint8')
            t[:, :, 0] = label[3, :, :]
            t[:, :, 1] = label[1, :, :]
            t[:, :, 2] = label[2, :, :]
            to_save_img = Image.fromarray(t)
            draw = ImageDraw.Draw(to_save_img)
            font = ImageFont.truetype("/usr/share/fonts/truetype/takao-gothic/TakaoGothic.ttf", 25)
            draw.text((50,50), ',\n'.join(linker_tags[head + '.jpg']['terms']), (255, 0, 0),font=font)
            to_save_img.save( 'out/preview/' + head + '.vec.jpg' )
            to_return_ = np.asarray(to_save_img.convert('RGB'))
            to_return = np.zeros((self.IN_CH, to_return_.shape[0], to_return_.shape[1])).astype('uint8')
            to_return[0, :, :] = to_return_[:, :, 0]
            to_return[1, :, :] = to_return_[:, :, 1]
            to_return[2, :, :] = to_return_[:, :, 2]
            to_return[3, :tagvec.shape[0], :tagvec.shape[1]] = tagvec
            self.dataset.append((img, to_return))
            self.dataset.append((img, to_return))
        print("load Vec-dataset done")
        return None
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
    def __len__(self):
        return len(self.dataset)


class VecDataset(dataset_mixin.DatasetMixin):
    def __init__(self, dataDir='./base', data_range=(1,100)):
        print("load Vec-dataset start")
        print("    from: %s"%dataDir)
        print("    range: [%d, %d)"%(data_range[0], data_range[1]))
        self.IN_CH = 4
        self.dataDir = dataDir
        self.dataset = []
        files = glob('./fonts/*')
        orgs = list(filter(lambda x:'.org.' in x, files))
        heads = []
        for org in orgs:
            print(org)
            heads.append( org.split('.')[1].split('/').pop() )
            print( org.split('.')[1].split('/').pop()  )
        for i in range(data_range[0],data_range[1]):
            head = heads[i]
            """
            headが入っているのが、jsonのキーにもなる
            """
            print(i, "/", data_range[1] - data_range[0], head)
            """
            meta tag vecを可変にする
            """
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
            """
            FIX : このパラメータで、メタ情報領域を生成する
            """
            FIX = 1
            red, grn, blu = lbl_[:,:,0], lbl_[:,:,1], lbl_[:,:,2]
            to_return = np.zeros((self.IN_CH, lbl_.shape[0], lbl_.shape[1])).astype('uint8')
            to_return[0, :, :] = lbl_[:, :, 0]
            to_return[1, :, :] = lbl_[:, :, 1]
            to_return[2, :, :] = lbl_[:, :, 2]
            #to_return[3, :tagvec.shape[0], :tagvec.shape[1]] = tagvec
            self.dataset.append((img, to_return))
        print("load Vec-dataset done")
    def __len__(self):
        return len(self.dataset)
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
