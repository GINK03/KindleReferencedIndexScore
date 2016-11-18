import sys
import os
import collections
a,b,c = map(int, input().strip().split(" ") )
m = max([a,b,c])  
num = 0
evals = []
cl = [a,b,c]
if cl[1] != cl[2] and cl[0] != cl[2]  and (min(cl) == b or max(cl) == b):
  print("INF")
  sys.exit(0)

for _ in range(2,m+1):
  a_ = a % _
  b_ = b % _
  c_ = c % _
  cl = [a_, b_, c_]
  if cl[0] == cl[1] == cl[2] or cl[0] == cl[1] or cl[1] == cl[2] or cl[0] == cl[2]:
    continue
  if cl[0] != cl[2]  and (min(cl) == b%_ or max(cl) == b%_):
    num += 1
    evals.append( "_".join(map(str,cl)) )
collect = collections.Counter(evals)
if len(collect.values()) == 0:
  print(0)
  sys.exit(0)
print( sum(collect.values()) )
