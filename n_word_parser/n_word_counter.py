# coding: utf-8
import os
import sys
import itertools
import re

all_terms = set()

targets = set(re.sub('\s{1,}', ' ', open('./top2000.ws').read().strip().replace('　', '')).split(' '))
print "今回のvocabサイズは", len(targets), "です"
for w in targets:
    #print w
    pass

result = {}
for line in sys.stdin:
    lines = line.strip().split('。')
    for one_line in lines:
        if result.get(one_line) != None:
            continue
        terms = one_line.split(' ')
        for term in terms:
            all_terms.add(term)

        for term in terms:
            if result.get(one_line) == None:
                result[one_line] = [0., 0.]
            if term in targets:
                result[one_line][0] += 1.
            else:
                result[one_line][1] += 1.

distinct_result = filter(lambda x:x[1][1] <= 5 and x[1][0] != 0 and x[1][0]/(x[1][1]+1) > 1. and (x[1][0] + x[1][1]) >= 10 , result.iteritems())
import json
for k, v in sorted(distinct_result, key=lambda x: x[1][0]/(x[1][1]+1.)*(-1.)) :
    print k, '|', json.dumps(v)



