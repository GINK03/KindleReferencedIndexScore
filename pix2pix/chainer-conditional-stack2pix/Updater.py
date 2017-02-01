#!/usr/bin/env python

from __future__ import print_function

import chainer
import chainer.functions as F
from chainer import Variable

import numpy as np
from PIL import Image

from chainer import cuda
from chainer import function
from chainer.utils import type_check
import numpy

class FacadeUpdater(chainer.training.StandardUpdater):

    def __init__(self, *args, **kwargs):
        self.enc, self.dec, self.dis = kwargs.pop('models')
        super(FacadeUpdater, self).__init__(*args, **kwargs)


    def loss_enc(self, enc, x_out, t_out, y_out, lam1=100, lam2=1):
        batchsize,_,w,h = y_out.data.shape
        loss_rec = lam1*(F.mean_absolute_error(x_out, t_out))
        loss_adv = lam2*F.sum(F.softplus(-y_out)) / batchsize / w / h
        loss = loss_rec + loss_adv
        chainer.report({'loss': loss}, enc)
        return loss
        
    def loss_dec(self, dec, x_out, t_out, y_out, lam1=100, lam2=1):
        batchsize,_,w,h = y_out.data.shape
        loss_rec = lam1*(F.mean_absolute_error(x_out, t_out))
        loss_adv = lam2*F.sum(F.softplus(-y_out)) / batchsize / w / h
        loss = loss_rec + loss_adv
        chainer.report({'loss': loss}, dec)
        return loss
        
        
    def loss_dis(self, dis, y_in, y_out):
        batchsize,_,w,h = y_in.data.shape
        
        L1 = F.sum(F.softplus(-y_in)) / batchsize / w / h
        L2 = F.sum(F.softplus(y_out)) / batchsize / w / h
        loss = L1 + L2
        chainer.report({'loss': loss}, dis)
        return loss

    def update_core(self):        
        enc_optimizer = self.get_optimizer('enc')
        dec_optimizer = self.get_optimizer('dec')
        dis_optimizer = self.get_optimizer('dis')
        
        enc, dec, dis = self.enc, self.dec, self.dis
        xp = enc.xp

        batch = self.get_iterator('main').next()
        batchsize = len(batch)
        in_ch = batch[0][0].shape[0]
        """ Edit g """
        """ operational vector$B$,(Bbatch[-1][0][-1][0]$B$G$"$k(B
        $B9=B$$,$d$?$iJ#;($J$N$G5$$r$D$1$k(B
        """
        #print("Batch size", len(batch))
        #print("Batch all", batch)
        #print("Batch [-1][0]", batch[-1][0])
        #print("Batch [-1][1]", batch[-1][1])
        #print("Batch [-1][0][-1][0]", batch[-1][0][-1][0])
        #print("Batch len([-1][0][-1])", len(batch[-1][0][-1][0]) )
        path_through = batch[-1][0][-1][0]
        """$B!!:G8e$N%$%s%G%C%/%9$K%"%/%;%9$7$F!">pJs$r<h$j=P$9(B """
        """ $B$3$l$O!"%P%C%A%5%$%:$,(B1$B$N$H$-$N$_M-8z$G$"$k$+$i$7$F!"5$$r$D$1$k$3$H(B """
        #path_through1 = []
        #for in_contain in batch[-1][0][-1]:
            #print("IN_CONTAIN", in_contain)
        #    for c in in_contain:
        #        path_through1.append(c)
        #print("path-through len", len(path_through1))
        """ $B$3$3$^$G(B """

        out_ch = batch[0][1].shape[0]
        w_in = 256
        w_out = 256
        
        x_in = xp.zeros((batchsize, in_ch, w_in, w_in)).astype("f")
        t_out = xp.zeros((batchsize, out_ch, w_out, w_out)).astype("f")
        
        for i in range(batchsize):
            x_in[i,:] = xp.asarray(batch[i][0])
            t_out[i,:] = xp.asarray(batch[i][1])
        x_in = Variable(x_in)
        
        z = enc(x_in, test=False)
        """ $B$3$N(Bz$B%Y%/%H%k$rJQ2=$5$;$l$P!"G$0U$NJ}8~@-$K;}$C$F$$$/$3$H$,$G$-$k(B """
        #print("z", z)
        """ Z$B$rD>@\JT=8$9$k$N$O4m81$J$N$G!"(Bdec$B$N0z?t$rA}$d$7$FBP=h$7$?$[$&$,NI$5$=$&(B """
        x_out = dec(z, path_through, test=False)
        #x_out = dec(z, test=False)

        y_fake = dis(x_in, x_out, test=False)
        y_real = dis(x_in, t_out, test=False)


        enc_optimizer.update(self.loss_enc, enc, x_out, t_out, y_fake)
        for z_ in z:
            z_.unchain_backward()
        dec_optimizer.update(self.loss_dec, dec, x_out, t_out, y_fake)
        x_in.unchain_backward()
        x_out.unchain_backward()
        dis_optimizer.update(self.loss_dis, dis, y_real, y_fake)
