
import os
import math
import itertools
import typing 
import sys
sys.setrecursionlimit(10000)
T = int(input())
S = [list(map(int, list(input()))) for _ in range(T)]
for s in S:
  def rec(s: list) -> None:
    if len(s) == 1:
        print(s.pop()) 
        return
    arr = [int(s) if len(s) == 1 else int(s[1]) + int(s[0]) for s in [str(p[0] + p[1]) for p in list(zip(s, s[1:]))]]
    return rec( arr )
  rec(s)
