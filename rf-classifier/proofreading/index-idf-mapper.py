# coding: utf-8
import os
import math
import sys
import json

term_index_idf = json.loads(open('./term-index-idf.json').read() )


for line in open('./posi.wakati.txt').read().split('\n'):
    line = line.strip()
    base = [0.0] * len(term_index_idf.keys())

    for t in line.split(' '):
        t = t.decode('utf-8')
        base[term_index_idf[t][0]] = term_index_idf[t][1]
    print json.dumps( [1, base] )

for line in open('./nega.wakati.txt').read().split('\n'):
    line = line.strip()
    base = [0.0] * len(term_index_idf.keys())

    for t in line.split(' '):
        t = t.decode('utf-8')
        base[term_index_idf[t][0]] = term_index_idf[t][1]
    print json.dumps( [0, base] )
