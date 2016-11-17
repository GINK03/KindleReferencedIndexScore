
import re
n = raw_input()
al = raw_input().strip()

while True:
  wr = []
  br = []
  for i in range(len(al)):
    for m in re.compile('bw{1,}b').finditer(al[i:]):
      h, t = m.span()
      h, t = h + 1 + i, t - 2 + i
      wr.append( (h, t) )
    for m in re.compile('wb{1,}w').finditer(al[i:]):
      h, t = m.span()
      h, t = h + 1 + i, t - 2 + i
      br.append( (h, t) )
  #print set(wr)
  #print set(br)
  nextstr = map(str, al)
  for rept in set(wr):
    s,e = rept
    for i in range(s,e+1):
      #print "w->b", i
      nextstr[i] = 'b'
  for rept in set(br):
    s,e = rept
    for i in range(s,e+1):
      #print "b->w", i
      nextstr[i] = 'w'

  if al == ''.join(nextstr):
    break
  al = ''.join(nextstr)
print al.count('b')
