def prime_table(n):
  plist = [True for _ in xrange(n + 1)]
  i = 2
  while i * i <= n:
    if plist[i]:
      j = i + i
      while j <= n:
        plist[j] = False
        j += i
    i += 1

  table = [i for i in xrange(n + 1) if plist[i] and i >= 2]
  return table

import sys
ia, ib =  raw_input().strip().upper().split(' ')
max_, step = int(ia), int(ib)

ptable = prime_table(max_)

for i in range(0, max_, step):
 fil = filter(lambda x:x <= i+step, ptable) 
 print str(i+1).zfill(len(str(max_))) + "-" + str(i+step).zfill(len(str(max_))) + ":" + "*"*len(fil)
 ptable = filter(lambda x:x > i+step, ptable)
