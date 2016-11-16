# coding: utf-8

import os
import math
import sys
import re
import jctconv

for line in sys.stdin:
    line = line.strip()
    line = re.sub('\d{1,}', 'number', line)
    print line.decode('utf-8')
