# coding: utf-8
import os
import sys
import math
import re

open('./dena.wakati.txt').read().split('\n')
open('./suumo.wakati.enum.txt').read().split('\n')
idf = {}
cnt = 0
import re
for line in (open('./dena.wakati.txt').read() + open('./suumo.wakati.enum.txt').read()).split('\n'):
    cnt += 1
    line = line.strip().lower()
    line = re.sub('\d{1,}', 'number', line)
    url = line.split(' ')[0]
    ts  = line.split(' ')[1:]
    for t in set(ts):
        if idf.get(t) == None:
            idf[t] = 1.
        else:
            idf[t] += 1.

for i, (t, f) in enumerate(sorted(idf.iteritems(), key=lambda x:x[1]*-1)):
    #print t, f
    idf[t] = [math.log( cnt / f ), i]

import json
open('./idf.json', 'w').write(json.dumps(idf))

for t, f in sorted(idf.iteritems(), key=lambda x:x[1]*-1):
    print t, f
