
n, m, z = map(int, input().split())
n = set(range(n, z+1, n))
m = set(range(m, z+1, m))
print(len(n.intersection(m)))


