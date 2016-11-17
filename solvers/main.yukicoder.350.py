from decimal import *
getcontext().prec = 12
ins = map(Decimal, map(float, raw_input().split(" ") ) )
print int(ins[0] * ins[1])
