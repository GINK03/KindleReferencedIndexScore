# coding: utf-8 

import json

obj = json.loads(open('./idf.json').read().strip())

for k, v in sorted(obj.iteritems(), key=lambda x:x[1]*-1):
    print k.encode('utf-8'), v
