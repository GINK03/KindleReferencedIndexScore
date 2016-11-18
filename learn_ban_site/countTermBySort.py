# coding: utf-8
# 必ずPython3で実行すること
import os
import math
import sys

buff = {}

for line in sys.stdin:
  for t in line.split(' '):
    if buff.get(t) == None:
       buff[t] = 1
    else:
       buff[t] += 1
          
print '全情報量', len(buff.keys())
print '1文字報量', len(filter(lambda x:x==1, buff.values() ) )
print '2文字報量', len(filter(lambda x:x==2, buff.values() ) )
print '5文字以下報量', len(filter(lambda x:x<=5, buff.values() ) )
for t in sorted(filter(lambda x:x[1]<=4, buff.iteritems()), key=lambda x:x[1]):
    print t[0]
