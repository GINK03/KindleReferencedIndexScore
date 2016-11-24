# coding: utf-8

import os
import math
import sys

term_num = {}
a = 0
for line in (open('./nega.wakati.txt').read() + open('./posi.wakati.txt').read()).split('\n'):
    a += 1
    line = line.strip()
    terms = set(line.split(' '))
    for term in terms:
        if term_num.get(term) == None:
            term_num[term] = 1
        else:
            term_num[term] += 1
idf = {}
for index, (term, num) in enumerate(term_num.iteritems()):
    if idf.get(term) == None:
        idf[term] = (index, math.log( a / num ) )

for term, (index, score) in idf.iteritems():
    print term, index, score

import json
open('term-index-idf.json', 'w').write(json.dumps(idf))
