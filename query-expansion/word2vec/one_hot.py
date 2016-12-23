# coding: utf-8
import sys
import json
try:
  import cPickle as P
except:
  import pickle as P
import re
from collections import Counter as C
from copy import deepcopy as dp
txt = open('./sample/pixiv201612.tag_txt.snapshot', encoding='utf-8').read().replace('\n', ' ')
txt = re.sub('\s{1,}', ' ', txt)
t_f = C( txt.split(' ') )

for t, f in sorted(t_f.items(), key=lambda x:x[1]*-1):
    #print(t, f)
    pass
ts = [t for t, f in sorted(t_f.items(), key=lambda x:x[1]*-1)]

print('max len', len(ts))
vectors = [0.] * 4098

term_vec = {}
cnt = 0
flag = False
for k in range(0, 1024):
    if flag == True: break
    for i in range(1025, 4098):
        vectors_ = [0.] * 4098
        vectors_[k] = 1.
        vectors_[i] = 1.
        if len(ts) <= cnt: 
            flag = True
            break
        term = ts[cnt]
        term_vec[term] = json.dumps(vectors_)
        cnt += 1

open('./vectorized.json', 'w').write(json.dumps(term_vec))

