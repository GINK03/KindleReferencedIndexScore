from __future__ import print_function
import os
import sys
from KindleReferencedIndexScoreNLPCommon import *
import redis
from KindleReferencedIndexScoreConfigMapper import *


import redis
r = redis.Redis(host=CM.REDIS_IP, port=6379, db=0)
META_ALREADY_CHECKED = '[@META_ALREADY_CAHCKED]'
already_checked = list()

if __name__ == '__main__' :
    raws = sys.argv[1:]
    qs = list()
    for raw in raws:
        qs.extend( make_query(raw) )
    print(' '.join(qs))
    ldic = []
    for q in qs:
        ldic.append( r.hgetall(q) )

  
    common_keys = set()
    #from itertools import chain
    #list(chain.from_iterable(l))
    for d in ldic:
        for x in d.keys():
            common_keys.add(x)
    rank_with = []

    res = {}
    for k in common_keys:
        for d in ldic:
            if res.get(k) == None:
                res.update({k:(lambda x:float(x) if x else 0.)(d.get(k) ) } )
            else:
                res[k] += (lambda x:float(x) if x else 0.)(d.get(k) )
    import itertools
    for k, v in itertools.islice(sorted( res.items(), key=lambda x:x[1]*-1), 0, 20):
        print('http://amazon.jp/dp/' + k,v)
            

