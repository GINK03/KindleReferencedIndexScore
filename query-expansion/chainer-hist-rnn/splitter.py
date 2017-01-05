# coding: utf-8
import re
import math
import os
import sys
import json
from collections import Counter as C
from itertools import chain
buff = []
stringbuff = ''
cnt = 1
TARGET_DIR = './data/tinyasahi/'
FILE_NAME  = 'asahi.txt.test.wakati'
def flash(buff):
    global cnt
    flatten = list(chain(*buff))
    obj = {}
    bow = {}
    for k, v in C(flatten).items():
        bow[k] = v
    obj['bow'] = bow
    obj['contents'] = flatten
    open(TARGET_DIR + str(cnt) + '.json', 'w').write(json.dumps(obj))
    #for t in flatten:
    #    print(t)
    buff = []
    stringbuff = ''
    cnt += 1
    return buff

for line in filter(lambda x:x != '', open(TARGET_DIR + FILE_NAME).read().split('\n')):
    buff.append(line.split(' '))
    stringbuff += line
    if 1024*1024*10 < sys.getsizeof(stringbuff):
        buff = flash(buff)
        stringbuff = ''

flash(buff)
