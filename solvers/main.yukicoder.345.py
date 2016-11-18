
import re
line = raw_input().strip()
l4 = []
for i in range(len(line)):
  l0 = re.findall("c.*?w.*?w", line[i:])
  l1 = re.findall("cw.*?w", line[i:])
  l2 = re.findall("c.*?ww", line[i:])
  l3 = re.findall("cww", line[i:])
  l4 = l4 + l0 + l1 + l2 + l3
import sys
#print l4
if len(l4) == 0:
  print -1
  sys.exit(0)
print sorted(map(len, l4)).pop(0)

