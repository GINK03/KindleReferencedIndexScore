#snakes = [[]] * 10
snakes = [[] for _ in range(10) ]
print(snakes)
snakes[1].append('蛇')
print(snakes)
