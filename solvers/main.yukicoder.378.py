import sys
import os

line = raw_input()
line = int(line)

head = [line]
i = line
for _ in xrange(line):
  i = i/2
  head.append(i)
  if i == 0:
    break
print line*2 - sum(head)
  
