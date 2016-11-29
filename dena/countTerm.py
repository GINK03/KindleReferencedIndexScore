# coding: utf-8
# 必ずPython3で実行すること
import os
import math
import sys

buff = []

for line in sys.stdin:
  buff.extend(line.strip().split(' '))

buff = set(buff)
for b in buff:
  print(b)
