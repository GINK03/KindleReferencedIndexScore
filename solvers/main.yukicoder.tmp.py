import re
l = raw_input()
def rep(x):
  if x == "+":
    x = "-"
  elif x == "-":
    x = "+"
  return x
l = re.sub("^\+(\d)", r"\1", l)
l = re.sub("(\d)-\+(\d)", r"\1-\2", l)
l = re.sub("(\d)\+\+(\d)", r"\1+\2", l)
l = re.sub("(\d)-(\d)", r"\1+-\2", l)
#print l
m = map(lambda x:rep(x), re.findall("\+|-?\d{1,}|-", l))
#print m
print eval("".join(m))

