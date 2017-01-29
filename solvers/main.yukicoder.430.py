s = input() 
m = int(input())
search = set()
[search.add(input()) for _ in range(m)]
maxlen = max(map(lambda x:len(x), search))
result = 0
for start in range(len(s)):
    for width in range(1, min(len(s) - start, maxlen) + 1):
        result += 1 if s[start:start+width] in search else 0
print(result)
