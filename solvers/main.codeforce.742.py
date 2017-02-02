import sys
order = int(input())

t = 8
if order == 0:
  print(1)
else:
  if order%4 == 1:
    print(8)
  elif order%4 == 2:
    print(4)
  elif order%4 == 3:
    print(2)
  elif order%4 == 0:
    print(6)



