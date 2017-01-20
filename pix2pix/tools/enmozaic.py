# coding: utf-8
from __future__ import print_function
import os
import math
import cv2
import sys
import glob
import numpy as np
import plyvel
import json
from os.path import exists
linkers = set()
c = 1
"""
for k, v in plyvel.DB('./cp/pixiv_htmls'):
    k = k.decode('utf-8')
    v = v.decode('utf-8')
    if 'URL' in k: continue
    try:
     o = json.loads(v)
    except:
     continue
    c += 1
    if '艦これ' in ''.join(o.get('tags')):
        linkers.add(o['linker'])
"""
for k, v in json.loads(open('../chainer-mozaic2pix/hoppou/linker_tags.json').read()).items():
    linkers.add(k)
    print(k)
sys.exit()
print('number of fleet girls', len(linkers), c)
source = 'ip'
target = 'ip2'
for e, fname in enumerate(glob.glob('./' + source + '/*.jpg')):
    im = cv2.imread(fname)
    if fname.split('/').pop() not in linkers:
        continue
    # すでにコンバート済み案件に関してはタッチしない
    outfname = './' + target + '/' + fname.split('/').pop()
    if exists(outfname + '.cnv.png') and exists(outfname + '.org.jpg'): 
        continue
    h, w, channels = im.shape
    if float(h)/w > 2 or float(h)/w < 0.5 : 
        print('サイズ比がおかしいです', fname )
        continue
    else:
        hen = min( [h, w] )
        r, g, b = 0., 0., 0.
        for i in range(hen):
            for j in range(hen):
                pixel = im[i, j]
                r += pixel[0]
                g += pixel[1]
                b += pixel[2]
        r = r/(hen**2)
        g = g/(hen**2)
        b = b/(hen**2)
        if sum(map(abs, [r - g, g - b, b - r ]) )  < 12. :
            print('モノクロの可能性があります、スキップします')
            continue
        gray = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(im, ksize=(21, 21), sigmaX=0, sigmaY=0) 
        inv  = 255 - blur
        dst_gray, dst_color = cv2.pencilSketch(im, sigma_s=250, sigma_r=0.07, shade_factor=0.05) 
        th3 = cv2.adaptiveThreshold(dst_gray,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,\
                            cv2.THRESH_BINARY,3,2)
        outfname = './' + target + '/' + fname.split('/').pop()
        color = ':'.join(map(str, [r,g,b]))
        #cv2.imwrite(outfname + '.cnv.png', th3)
        #cv2.imwrite(outfname + '.org.jpg', im)
        print(e, fname)
        print(e, outfname)
