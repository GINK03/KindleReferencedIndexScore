#!/usr/bin/env python

from __future__ import print_function

import numpy as np
import cupy as cp
import chainer.functions as F
from chainer import Variable
import chainer
from chainer import cuda
import chainer.functions as F
import chainer.links as L

# U-net https://arxiv.org/pdf/1611.07004v1.pdf

# convolution-batchnormalization-(dropout)-relu
class CBR(chainer.Chain):
    def __init__(self, ch0, ch1, bn=True, sample='down', activation=F.relu, dropout=False):
        self.bn = bn
        self.activation = activation
        self.dropout = dropout
        layers = {}
        w = chainer.initializers.Normal(0.02)
        if sample=='down':
            layers['c'] = L.Convolution2D(ch0, ch1, 4, 2, 1, initialW=w)
        else:
            layers['c'] = L.Deconvolution2D(ch0, ch1, 4, 2, 1, initialW=w)
        if bn:
            layers['batchnorm'] = L.BatchNormalization(ch1)
        super(CBR, self).__init__(**layers)
        
    def __call__(self, x, test):
        h = self.c(x)
        if self.bn:
            h = self.batchnorm(h, test=test)
        if self.dropout:
            h = F.dropout(h)
        if not self.activation is None:
            h = self.activation(h)
        return h
    
class Encoder(chainer.Chain):
    def __init__(self, in_ch):
        layers = {}
        w = chainer.initializers.Normal(0.02)
        layers['c0'] = F.Convolution2D(in_ch, 64, 3, 1, 1, initialW=w)
        layers['c1'] = CBR(64, 128, bn=True, sample='down', activation=F.leaky_relu, dropout=False)
        layers['c2'] = CBR(128, 256, bn=True, sample='down', activation=F.leaky_relu, dropout=False)
        layers['c3'] = CBR(256, 512, bn=True, sample='down', activation=F.leaky_relu, dropout=False)
        layers['c4'] = CBR(512, 512, bn=True, sample='down', activation=F.leaky_relu, dropout=False)
        layers['c5'] = CBR(512, 512, bn=True, sample='down', activation=F.leaky_relu, dropout=False)
        layers['c6'] = CBR(512, 512, bn=True, sample='down', activation=F.leaky_relu, dropout=False)
        layers['c7'] = CBR(512, 512, bn=True, sample='down', activation=F.leaky_relu, dropout=False)
        super(Encoder, self).__init__(**layers)

    def __call__(self, x, test=False):
        hs = [F.leaky_relu(self.c0(x))]
        for i in range(1,8):
            hs.append(self['c%d'%i](hs[i-1], test=test))
        return hs

class Decoder(chainer.Chain):
    def __init__(self, out_ch):
        self.EXTRA_VECTOR = 256
        layers = {}
        w = chainer.initializers.Normal(0.02)
        layers['c0'] = CBR(512 + self.EXTRA_VECTOR, 512 + self.EXTRA_VECTOR, bn=True, sample='up', activation=F.relu, dropout=True)
        # layers['c0'] = CBR(512, 512, bn=True, sample='up', activation=F.relu, dropout=True)
        layers['c1'] = CBR(1024 + self.EXTRA_VECTOR, 512, bn=True, sample='up', activation=F.relu, dropout=True)
        layers['c2'] = CBR(1024, 512, bn=True, sample='up', activation=F.relu, dropout=True)
        layers['c3'] = CBR(1024, 512, bn=True, sample='up', activation=F.relu, dropout=False)
        layers['c4'] = CBR(1024, 256, bn=True, sample='up', activation=F.relu, dropout=False)
        layers['c5'] = CBR(512, 128, bn=True, sample='up', activation=F.relu, dropout=False)
        layers['c6'] = CBR(256, 64, bn=True, sample='up', activation=F.relu, dropout=False)
        layers['c7'] = F.Convolution2D(128, out_ch, 3, 1, 1, initialW=w)
        super(Decoder, self).__init__(**layers)

    def __call__(self, hs, path_through, test=False):
        """ zのフォーマットはshape(1, 512, 2, 2)となっており、512bitが最大値だと思われる """
        """ 
        path_throughのフォーマットはshape(256)なので、全然足りない
        4倍して,2,2で切って、代入する
        """
        path_through_4 = cp.repeat(path_through, 4).astype('float32')
        path_through_2x2 = chainer.cuda.to_gpu(cp.reshape(path_through_4, (1, 256, 2, 2)) )
        #print("orig shape.", hs[-1].shape)
        #print("tag shape.", path_through_2x2.shape)
        #print("tag object.", type(path_through_2x2))
        #print("shape, ", type(hs), type(hs[-1]))
        hs[-1] = F.concat( (hs[-1], Variable(path_through_2x2)) )
        """
        - device: <CUDA Device 0>
        - volatile: OFF
        - backend: <class 'cupy.core.core.ndarray'>
        - shape: (1, 512, 2, 2)
        - dtype: float32
        """
        #cupy.concat(hs[-1],) 
        """
        import numpy as np
        import cupy as cp
        import cupy.manipulation.join as cujoin
        from chainer import Variable
        cucat = cujoin.concatenate
        path_through
        for i in range(len(path_through)-4):
            p1, p2, p3, p4 = path_through[i:i+4]
            sample = cp.array([[[[p1, p2], [p3, p4]]]]).astype('float32')
            break
        #print( sample.shape )
        vsample = Variable(sample)
        import chainer.functions.array.concat as cat
        hs[-1] = cat.concat([hs[-1], vsample])
        """
        #print("hs", hs[-1], hs[-1].__len__(), hs[-1].debug_print())
        h = self.c0(hs[-1], test=test)
        for i in range(1,8):
            h = F.concat([h, hs[-i-1]])
            if i<7:
                h = self['c%d'%i](h, test=test)
            else:
                h = self.c7(h)
        return h

    
class Discriminator(chainer.Chain):
    def __init__(self, in_ch, out_ch):
        layers = {}
        w = chainer.initializers.Normal(0.02)
        layers['c0_0'] = CBR(in_ch, 32, bn=False, sample='down', activation=F.leaky_relu, dropout=False)
        layers['c0_1'] = CBR(out_ch, 32, bn=False, sample='down', activation=F.leaky_relu, dropout=False)
        layers['c1'] = CBR(64, 128, bn=True, sample='down', activation=F.leaky_relu, dropout=False)
        layers['c2'] = CBR(128, 256, bn=True, sample='down', activation=F.leaky_relu, dropout=False)
        layers['c3'] = CBR(256, 512, bn=True, sample='down', activation=F.leaky_relu, dropout=False)
        layers['c4'] = F.Convolution2D(512, 1, 3, 1, 1, initialW=w)
        super(Discriminator, self).__init__(**layers)

    def __call__(self, x_0, x_1, test=False):
        h = F.concat([self.c0_0(x_0, test=test), self.c0_1(x_1, test=test)])
        h = self.c1(h, test=test)
        h = self.c2(h, test=test)
        h = self.c3(h, test=test)
        h = self.c4(h)
        #h = F.average_pooling_2d(h, h.data.shape[2], 1, 0)
        return h
