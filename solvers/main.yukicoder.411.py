N, K = map(int, input().split())
baseline = 2**(N-K)
print( baseline if K!=1 else baseline - N)
