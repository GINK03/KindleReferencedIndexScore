import sys
import math

line = raw_input().strip()
print  min([line.count("t"), line.count("r"), line.count("e")/2])
