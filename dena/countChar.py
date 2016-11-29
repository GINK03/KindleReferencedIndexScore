# coding: utf-8
# 必ずPython3で実行すること
import os
import math
import sys

buff = ''

for line in sys.stdin:
  buff += line.strip()

buff = set(list(buff))
for b in buff:
  print(b)
