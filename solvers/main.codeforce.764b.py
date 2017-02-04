
import os
import sys
import math
import itertools

#l =  [2, 3, 9, 6, 7, 1, 4]

N = int(input())
l = list(map(int, input().split()))

i = 0
LEN = len(l)
while i < LEN -i -1:
  if i%2 == 0:
    l[i], l[LEN -i -1] = l[LEN -i -1], l[i]
  i += 1
print(' '.join(map(str, l)))
