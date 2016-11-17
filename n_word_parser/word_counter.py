# coding: utf-8
import os
import math
import sys
import itertools

if '--create' in sys.argv:
    t_f = {}
    alls = open('./wakati.txt').read().split('\n')
    for text in alls:
        text = text.strip()
        terms = text.split(' ')
        for term in terms:
            if t_f.get(term) == None:
                t_f[term] = 0
            else:
                t_f[term] += 1

    import json
    f = open('./t_f.json', 'w')
    f.write(json.dumps(t_f))
    f.close()

if '--dump' in sys.argv:
   import json
   t_f = json.loads(open('./t_f.json').read())
  
   """
   for k, v in sorted(t_f.iteritems(), key=lambda x:x[1]*(-1))[:2000]:
        #print k.encode('utf-8'), v
        print k.encode('utf-8'), 
   """
   for k, v in sorted(t_f.iteritems(), key=lambda x:len(x[0])*(-1))[:100]:
       print k.encode('utf-8'), len(k.encode('utf-8'))
