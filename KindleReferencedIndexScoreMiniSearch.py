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
 
    term = set()
    ldic = []
    common_asins = set()
    for q in qs:
        dic = r.hgetall(q)
        ldic.append( dic )
        [common_asins.add(asin) for asin in  dic.keys()]
        print(q, dic.keys() ) 
    #from itertools import chain
    #list(chain.from_iterable(l))
    
    rank_with = []

    res = {}
    for asin in common_asins:
        for dic in ldic:
            if res.get(asin) == None:
                res.update({asin:(lambda x:float(x) if x else 0.)(dic.get(asin) ) } )
            else:
                res[asin] += (lambda x:float(x) if x else 0.)(dic.get(asin) )

    import itertools
    for k, v in sorted( res.items(), key=lambda x:x[1]*-1)[:20]:
        print('http://amazon.jp/dp/' + k,v)
            

