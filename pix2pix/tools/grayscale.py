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
for k, v in json.loads(open('./linker_tags.json').read()).items():
    linkers.add(k)

print('number of fleet girls', len(linkers), c)
source = 'kancolle.toho.fgo'
target = 'ip'
for e, fname in enumerate(glob.glob('./' + source + '/*.jpg')):
    # すでにコンバート済み案件に関してはタッチしない
    if exists(outfname + '.cnv.png') and exists(outfname + '.org.jpg'): 
        continue
    im = cv2.imread(fname)
    if fname.split('/').pop() not in linkers:
        continue
    h, w, channels = im.shape
    if float(h)/w > 2 or float(h)/w < 0.5 : 
        print('サイズ比がおかしいです', fname )
        continue
    else:
        hen = min( [h, w] )
        """
        # リサイザ、特に必要ないと思われるので一時的に無効にする
        if h > hen:
            im = im[h/2 - hen/2:h/2 + hen/2, :]
        else:
            im = im[:, w/2 - hen/2:w/2 + hen/2]
        """
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
        """
        kernel = np.ones((1,1),np.uint8)
        rosion = cv2.morphologyEx(th3, cv2.MORPH_CLOSE, kernel)
        th2 = cv2.adaptiveThreshold(im, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 3)
        edges = cv2.blur(gray, (3, 3))
        edges = gray
        edges = cv2.Canny(dst_gray, 100, 100, apertureSize=3)
        kernel = numpy.ones((3,3), dtype=numpy.float) / 12.0
        edges = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
        shifted = cv2.pyrMeanShiftFiltering(im, 5, 100)
        shifted = cv2.cvtColor(shifted,cv2.COLOR_BGR2GRAY)
        result = cv2.subtract(shifted, edges)
        invedges = 255 - edges
        """
        outfname = './' + target + '/' + fname.split('/').pop()
        color = ':'.join(map(str, [r,g,b]))
        cv2.imwrite(outfname + '.cnv.png', th3)
        cv2.imwrite(outfname + '.org.jpg', im)
        print(e, fname)
        print(e, outfname)
