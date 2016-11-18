def arithmetic_progression():
  return [ (lambda y: lambda x: y*x)(i) for i in range(1, 11)]
for func in arithmetic_progression():
    print(func(2), end=', ')
print()
for func in arithmetic_progression():
    print(func(10), end=', ')
print()
diff = int(input())
for func in arithmetic_progression():
    print(func(int(diff)), end=', ')
print()
