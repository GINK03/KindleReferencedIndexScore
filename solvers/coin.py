def find_changes(n, coins):
    if n < 0:
        return []
    if n == 0:
         return [[]]
    all_changes = []

    for last_used_coin in coins:
        combos = find_changes(n - last_used_coin, coins)
        for combo in combos:
            combo.append(last_used_coin)
            all_changes.append(combo)

    return all_changes

print find_changes(4, [1,2,3])
