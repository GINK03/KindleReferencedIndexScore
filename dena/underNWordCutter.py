# coding: utf-8

import math
import os
import sys

raws = filter(lambda x:x!='', open('./under5words.txt.mecab').read().split('\n') )
term_pats = [ (t[0], t[1].split(',')[1]) for t in [r.split('\t') for r in raws] ]

for t in term_pats:
  print t

for line in sys.stdin:
    line = line.strip()

