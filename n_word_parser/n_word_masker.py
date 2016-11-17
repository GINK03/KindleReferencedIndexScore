# coding: utf-8
import os
import sys
import itertools
import re

targets = set(re.sub('\s{1,}', ' ', open('./top2000.ws').read().strip().replace('　', '')).split(' '))
print "今回のvocabサイズは", len(targets), "です"
for w in targets:
    #print w
    pass

import json
for line in sys.stdin:
    lines = line.strip().split(' | ')
    context = lines[0]
    contexts = context.split(' ')
    rebuild = []
    for term in contexts:
        if term in targets:
            rebuild.append(term)
        else:
            rebuild.append('UNK')

    print ' '.join(rebuild)


