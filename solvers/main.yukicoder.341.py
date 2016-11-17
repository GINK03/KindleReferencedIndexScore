# coding: utf-8
import re
import sys
line = input().strip()
matchs =  re.findall("…{1,}", line)
lens = sorted(map(len, matchs))
if lens == []:
  print(0)
  sys.exit(0)
print(lens.pop())
