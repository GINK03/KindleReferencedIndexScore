import os

import numpy
from PIL import Image
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
    
class GGGDataset(dataset_mixin.DatasetMixin):
    def __init__(self, dataDir='./base', data_range=(1,300)):
        from glob import glob as g
        print("load GGG-dataset start")
        print("    from: %s"%dataDir)
        print("    range: [%d, %d)"%(data_range[0], data_range[1]))
        self.IN_CH = 4
        self.dataDir = dataDir
        self.dataset = []
        files = g('./hoppou/*')
        orgs = list(filter(lambda x:'.org.' in x, files))
        heads = []
        for org in orgs:
            heads.append( '.'.join(org.split('.')[1:5]).split('/').pop() )
        import json
        linker_tags = json.loads(open('./hoppou/linker_tags.json').read())
        for i in range(data_range[0],data_range[1]):
            head = heads[i]
            """
            headが入っているのが、jsonのキーにもなる
            """
            print(i, "/", data_range[1] - data_range[0], head)
            #print("head", head)
            tagvec = np.array(linker_tags[head + '.jpg']['vector'])
            #print("tagvec", tagvec)
            """
            meta tag vecを可変にする
            """
            #tagvec = np.repeat(tagvec, 256)
            #tagvec = np.resize(tagvec, (286, 286))
            #np.set_printoptions(threshold=np.nan)
            tagvec = np.resize(tagvec, (256,256) )
            #tagvec = np.repeat(tagvec,256)
            """
            確実に見える素性にするために、255倍する
            """
            tagvec *= 255

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
            #frombuffer = Image.frombuffer(data=lbl_, size=(img.shape[1], img.shape[2]), mode='RGB')
            """
            FIX : このパラメータで、メタ情報領域を生成する
            """
            FIX = 1
            red, grn, blu = lbl_[:,:,0], lbl_[:,:,1], lbl_[:,:,2]
            """
            ここで、スタンダライゼーションを行う
            """
            #red = (red - red.mean())/red.std()
            #grn = (grn - grn.mean())/grn.std()
            #blu = (blu - blu.mean())/blu.std()
            #>>> inser = np.array([[11, 12], [21, 22]])
	    #>>> zeros = np.zeros(9).reshape( (3,3) )
	    #>>> inser
	    #array([[11, 12],
       	    #[21, 22]])
	    #   >>> zeros
	    #array([[ 0.,  0.,  0.],
            #	[ 0.,  0.,  0.],
       	    #[ 0.,  0.,  0.]])
	    #  >>> zeros[:inser.shape[0], :inser.shape[1]] = inser
            # >>> zeros
            #    array([[ 11.,  12.,   0.],
            #     [ 21.,  22.,   0.],
            #     [  0.,   0.,   0.]])
            #print(tagvec)

            t = np.zeros((self.IN_CH, lbl_.shape[0], lbl_.shape[1])).astype('uint8')
            #print( "red", red.size, red.shape, red)
            t[0, :, :] = red
            t[1, :, :] = grn
            t[2, :, :] = blu
            t[3, :tagvec.shape[0], :tagvec.shape[1]] = tagvec
            #print(t[:,:,3])
            #w, h, _ = lbl_.shape
            #frombuffer = Image.frombuffer(data=t, size=(w, h), mode='RGB')
            #frombuffer.save('test.png')

            label = np.zeros((self.IN_CH, img.shape[1], img.shape[2])).astype("i")
            for j, e in [(0, red), (1, grn), (2, blu), (3, tagvec)]:
                if j == 3:
                  print("Enter meta execution")
                  label[j,:tagvec.shape[0], :tagvec.shape[1]] = tagvec
                else:
                  label[j,:] = e 

            """
            for j in range(self.IN_CH):
                    print("その他の処理です")
                    label[j,:] = label_==j
            """
            self.dataset.append((img,label))
            Image.fromarray(t, mode='RGB').save( 'out/preview/test.png' )
            
            
        """
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
        """
        print("load GGG-dataset done")
    
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

if __name__ == '__main__':
    ggg = GGGDataset( None )
