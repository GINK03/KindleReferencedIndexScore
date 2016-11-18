
import sys
import os

import math
import copy
import re
line = raw_input().strip()

line = line.replace("min", "mi@n")
mins = re.findall("mi.*?n", line)

print len(mins)
