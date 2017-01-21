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
source = './kancolle.toho.fgo'
target = 'pics'
for k, v in json.loads(open('./linker_tags.json').read()).items():
    linkers.add(k)
    print(k)
print('number of fleet girls', len(linkers), c)
for e, fname in enumerate(glob.glob('./' + source + '/*.jpg')):
    if fname.split('/').pop() not in linkers:
        continue
    im = cv2.imread(fname)
    print( fname )
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
        ensmall = cv2.resize(im, (int(w/10), int(h/10) ) )
        enlarge = cv2.resize(ensmall, (w, h), interpolation=cv2.INTER_NEAREST )
        if sum(map(abs, [r - g, g - b, b - r ]) )  < 12. :
            print('モノクロの可能性があります、スキップします')
            continue
        cv2.imwrite(outfname + '.cnv.png', enlarge)
        cv2.imwrite(outfname + '.org.jpg', im)
        print(e, fname)
        print(e, outfname)
