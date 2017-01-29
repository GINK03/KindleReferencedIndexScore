
n,k = map(int, input().split())
num = n - k - 2
result = [1, 3]
for _ in range(num):
    if result[-1] == 3 : 
        result.append(2)
        continue
    if result[-1] == 2 : 
        result.append(4)
        continue
    if result[-1] == 4 : 
        result.append(1)
        continue
    if result[-1] == 1 : 
        result.append(3)
        continue

for _ in range(k):
    result.append(result[-1])

print(' '.join(map(str, result)))
