#!/usr/bin/env python

import os

import numpy as np
from PIL import Image

import chainer
import chainer.cuda
from chainer import Variable

def out_image(updater, enc, dec, rows, cols, seed, dst, in_ch=12):
    @chainer.training.make_extension()
    def make_image(trainer):
        np.random.seed(seed)
        n_images = rows * cols
        xp = enc.xp
        
        w_in = 256
        w_out = 256
        out_ch = 3
        
        in_all = np.zeros((n_images, in_ch, w_in, w_in)).astype("i")
        gt_all = np.zeros((n_images, out_ch, w_out, w_out)).astype("f")
        gen_all = np.zeros((n_images, out_ch, w_out, w_out)).astype("f")
        
        for it in range(n_images):
            batch = updater.get_iterator('test').next()
            batchsize = len(batch)

            x_in = xp.zeros((batchsize, in_ch, w_in, w_in)).astype("f")
            t_out = xp.zeros((batchsize, out_ch, w_out, w_out)).astype("f")

            for i in range(batchsize):
                x_in[i,:] = xp.asarray(batch[i][0])
                t_out[i,:] = xp.asarray(batch[i][1])
            x_in = Variable(x_in)

            z = enc(x_in, test=False)
            x_out = dec(z, test=False)
            
            in_all[it,:] = x_in.data.get()[0,:]
            gt_all[it,:] = t_out.get()[0,:]
            gen_all[it,:] = x_out.data.get()[0,:]
        
        
        def save_image(x, name, mode=None):
            _, C, H, W = x.shape
            x = x.reshape((rows, cols, C, H, W))
            x = x.transpose(0, 3, 1, 4, 2)
            if C==1:
                x = x.reshape((rows*H, cols*W))
            else:
                x = x.reshape((rows*H, cols*W, C))

            preview_dir = '{}/preview'.format(dst)
            preview_path = preview_dir +\
                '/image_{}_{:0>8}.png'.format(name, trainer.updater.iteration)
            if not os.path.exists(preview_dir):
                os.makedirs(preview_dir)
            Image.fromarray(x, mode=mode).convert('RGB').save(preview_path)
        
        x = np.asarray(np.clip(gen_all * 128 + 128, 0.0, 255.0), dtype=np.uint8)
        save_image(x, "gen")
        
        #x = np.ones((n_images, 3, w_in, w_in)).astype(np.uint8)*255
        ## ANCHOR
        x = np.ones((w_in, w_in, 3)).astype(np.uint8)*255
        xs1 = None
        xs2 = None
        xs3 = None
        xs4 = None
        xs5 = None
        G_FIX = 1
        for _ in range(25):
            for i in range(in_ch - G_FIX):
              x[:,:,i] = np.uint8(in_all[_][i,:,:])
            if _ < 5:
              if xs1 is None:
                xs1 = x
                continue
              else:
                xs1 = np.concatenate( (xs1, x), axis = 1)
                continue
            elif _ < 10:
              if xs2 is None:
                xs2 = x
                continue
              else:
                xs2 = np.concatenate( (xs2, x), axis = 1)
                continue
            elif _ < 15:
              if xs3 is None:
                xs3 = x
                continue
              else:
                xs3 = np.concatenate( (xs3, x), axis = 1)
                continue
            elif _ < 20:
              if xs4 is None:
                xs4 = x
                continue
              else:
                xs4 = np.concatenate( (xs4, x), axis = 1)
                continue
            elif _ < 25:
              if xs5 is None:
                xs5 = x
                continue
              else:
                xs5 = np.concatenate( (xs5, x), axis = 1)
                continue
        xs = np.concatenate( (xs1, xs2, xs3, xs4, xs5), axis = 0 )
        # edit and hack
        # save_image(x, "in", mode='RGB')
        Image.fromarray(xs, mode='RGB').save('out/preview/image_in_' + \
                str(trainer.updater.iteration) + '.png')
        
        x = np.asarray(np.clip(gt_all * 128+128, 0.0, 255.0), dtype=np.uint8)
        save_image(x, "gt")
        
    return make_image
