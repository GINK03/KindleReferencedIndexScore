# coding: utf-8

import re
import math
import os
import sys

filename = sys.argv[1]

text = open(filename).read().split('\n')[0]

# d f g
for rep in [(r'<', '_<_'), (r'>', '_>_'), ('\+', '_+_'), ('\-', '_-_'), \
        (r'(a|d|f|g)', r'_\1_'), (r'(l\d{1,})', r'_\1_'), (r'(q\d{1,})', r'_\1_'), \
        (r'\.', '_._'), ('\^1', '_^1_')]:
    text = re.sub(rep[0], rep[1], text)
# distict underbar
text = re.sub('_{1,}', '_', text)
print(text)

open("%s/input.txt"%'/'.join(filename.split('/')[:-1]), 'w').write(text)
