# coding: utf-8

import os
import math
import sys
import re


idf = {}
cnt = 1
for line in open('./d1000.svm').read().split('\n'):
    line = line.strip()
    ents = line.split(' ')
    cnt += 1
    for ent in ents[2:]:
        print(ent)
        t = ent.split(':')[0]
        if idf.get(t) == None:
            idf[t] = 1
        else:
            idf[t] += 1
     

for t, f in idf.items():
    idf[t] = math.log( float(cnt)/f )
import json
open('idf.json', 'w').write(json.dumps(idf))

for t, f in sorted(idf.items(), key=lambda x:x[1]*-1):
    print(t, f)
