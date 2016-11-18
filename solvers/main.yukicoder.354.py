import sys
import os
import collections
import math

def prime_table(n):
  list = [True for _ in xrange(n + 1)]
  i = 2
  while i * i <= n:
    if list[i]:
      j = i + i
      while j <= n:
        list[j] = False
        j += i
    i += 1

  table = [i for i in xrange(n + 1) if list[i] and i >= 2]
  return table

from decimal import *
getcontext().prec = 28
al = []
def may_mel(p):
  d = Decimal(Decimal(2)**p-1)
  while True:
    #a = d%Decimal(2)
    d /= Decimal(2)
    if d == 0:
      break

def may_mel2(p):
  #bi = [0 for b in range(p)]
  print(p)
may_mel2(int(input()))
