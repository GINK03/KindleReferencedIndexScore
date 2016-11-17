import sys
import os
import itertools
import math

N, K = map(int, raw_input().split(" "))

for oon in itertools.permutations(range(1,N+1)):
 print oon
