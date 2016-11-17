
import sys
import re
def m(w):
  t2, t1 = w[-2:], w[-1]
  if t1 in ['s', 'o', 'x'] or t2 in ['sh', 'ch']:
    print w+'es'
    return
  
  if t1 in ['f']:
    print w[:-1] + 'ves'
    return

  if t2 in ['fe']:
    print w[:-2] + 'ves'
    return

  t2_2 = w[-2]
  if t1 in ['y'] and t2_2 not in ['a', 'i', 'u', 'e', 'o']:
    print w[:-1] + 'ies'
    return

  print w + 's'

N = int(raw_input())
for _ in range(N):
  m(raw_input().strip())


