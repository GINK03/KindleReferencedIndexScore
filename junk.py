import os, sys
import itertools
for line in sys.stdin:
    line.strip()
    print ' '.join(line.split(' ')[0:50000] )

