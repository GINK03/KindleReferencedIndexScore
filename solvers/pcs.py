import operator as op
def ncr(n, r):
    r = min(r, n-r)
    if r == 0: return 1
    numer = reduce(op.mul, xrange(n, n-r, -1))
    denom = reduce(op.mul, xrange(1, r+1))
    return numer//denom

N = int(raw_input())
seedlist = []
#build
import math
for i in range(N+1):
   if i == 0:
      seedlist.append(1)
   elif i == 1:
       seedlist.append(0)
   elif i == 2:
        seedlist.append(1)
   elif i == 3:
        seedlist.append(2)
   else:
        combi = [ (i, _) for _ in range(i, 0, -1)]
        NCR = [ ncr(c[0], c[1]) for c in combi ]
        SUM = sum([c2[0] * c2[1] for c2 in zip(seedlist, NCR)] )
        next = math.factorial(i) - SUM
        seedlist.append(next)
print seedlist.pop()

