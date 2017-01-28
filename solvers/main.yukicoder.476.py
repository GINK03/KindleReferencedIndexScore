
_, a = input().split()
xs = list(map(int, input().split()))
if float(a) == sum(xs)/len(xs):
    print("YES")
else:
    print("NO")
