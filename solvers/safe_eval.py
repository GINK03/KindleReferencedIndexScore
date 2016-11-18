two = 2
def mod(x,y):
  return x%y
def sumsq(*args):
 return sum(map(lambda x:x**2, list(args) ) )

max = None
abs = None
ia = raw_input().strip()
if ',,' in ia:
  print "Unknown syntax"
try:
  print eval(ia)
except SyntaxError, e: 
  if """unexpected EOF while parsing""" in e:
    print "Unknown syntax"
except NameError, e: 
  print "Unknown name"
  """name 'hoge' is not defined"""
except TypeError, e:
  print "Unknown name"
