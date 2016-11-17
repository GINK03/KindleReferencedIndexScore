
import sys
import os

import math
import copy
num = 0
for i, line in enumerate(sys.stdin):
 if i == 0:
   num = int(line)
   continue
 line = line.strip()
 li = map(int ,filter(lambda x:x != '', line.split(" ")))
 li = sorted(li)
 li2 = copy.copy(li)
 li2.insert(0, 0)
 binded = [bind[0] - bind[1] for bind in zip(li, li2)]
 binded.pop(0)
 head = binded[0]
 if head == 0:
  print "NO"
  sys.exit(0)
 for b in binded:
   if b != head:
     print "NO"
     sys.exit(0)
 print "YES"
