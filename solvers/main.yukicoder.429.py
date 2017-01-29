
N, K, X = map(int, input().split() )
ops = [list(input().split()) for _ in range(K)]
result = list(map(lambda x:int(x)-1, input().split())  )

heads = list(map(lambda x:list(map(lambda x2:int(x2)-1,x)), ops[:X-1]))
tails = list(map(lambda x:list(map(lambda x2:int(x2)-1,x)), reversed(ops[X:])) )
def swapper(target:list, op:list) -> None:
    target[op[0]], target[op[1]] = target[op[1]], target[op[0]]

target = [i for i in range(N)]
[swapper(target, op) for op in heads]

[swapper(result, op) for op in tails]

print(' '.join(list(map(lambda x:str(x+1), filter(lambda x:x is not None, map(lambda x2:x2[2] if x2[0] != x2[1] else None, zip(target, result, range(N))))))))
