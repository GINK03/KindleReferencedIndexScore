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
import sys
b = prime_table(10**6)

M = int(raw_input())
for prime in b:
  if M%prime == 0:
     print prime, M/prime
     sys.exit(0)

print "1", M
