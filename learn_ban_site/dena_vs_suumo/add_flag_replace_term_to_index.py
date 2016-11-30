

import os
import math
import sys
import json
import re
import collections
from collections import Counter
idf = json.loads(open('./idf.json').read())

for filename, flag in [('./dena.wakati.txt', 1), ('./suumo.wakati.enum.txt' , 0)]:
  for line in open(filename).read().split('\n'):
    line = line.strip().lower()
    try:
      line = re.sub('\d{1,}', 'number', line)
    except:
      continue
    cnt = Counter(line.split(' ')[1:])
    buff = []
    for (t, f) in cnt.items():
        t = t.decode('utf-8')
        try:
          buff.append( [idf[t][1], ':'.join(map(str, [idf[t][1]+1,idf[t][0]*f]))] )
          pass
        except:
          pass
    print flag,
    for tp in sorted(buff, key=lambda x:x[0]):
        print tp[1],
    print 
