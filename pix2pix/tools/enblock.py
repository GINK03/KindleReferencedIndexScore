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
import copy
from os.path import exists
import random
linkers = set()
source = 'hoppou'
target = 'pics'
STEP = 5
for k, v in json.loads(open('./linker_tags.json').read()).items():
    linkers.add(k)
    #print(k)
print('number of fleet girls', len(linkers))
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
        copyed = copy.copy( im ) 
        for _h in range(0, h, STEP):
            for _w in range(0, w, STEP):
                if random.random() >= 0.5:
                    cv2.rectangle(copyed, (_w, _h), (_w+STEP, _h+STEP), (255,255,255), -1 )
        if sum(map(abs, [r - g, g - b, b - r ]) )  < 12. :
            print('モノクロの可能性があります、スキップします')
            continue
        cv2.imwrite(outfname + '.cnv.png', copyed)
        cv2.imwrite(outfname + '.org.jpg', im)
        print(e, fname)
        print(e, outfname)
