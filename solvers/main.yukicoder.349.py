import itertools

swap = {
  "ne":"a",
  "ushi":"b",
  "tora":"c",
  "u":"d",
  "tatsu":"e",
  "mi":"f",
  "uma":"g",
  "hitsuji":"i",
  "saru":"j",
  "tori":"k",
  "inu":"l",
  "i":"n"
}
import collections
import sys
count = collections.Counter
tgts = []
for _ in range(int(raw_input())):
  i = raw_input()
  tgts.append(swap[i]) 
#print count(tgts)
noise = sorted(count(tgts).values()).pop()
ents =  sum(count(tgts).values()) - noise
if noise >= ents + 2: 
  print "NO"
  sys.exit(0)
print "YES"
"""
combis = map(lambda x:"".join(x), zip(swap.values(), swap.values()))
for pm in itertools.permutations( tgts):
  buff = False
  for c in combis:
    buff = c in "".join(pm)
  if buff == False:
    print "YES"
    sys.exit(0)
print "NO"
"""

