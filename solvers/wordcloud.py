import re
import sys
import math
for line in sys.stdin:
  line = line.strip()
  data = line.split(" ")
  data.pop(0)
  word, num = data[0], int(data[1])
  print( (word + " ")* int(math.log10( num )) )
