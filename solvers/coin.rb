def find_changes(n, coins)
    if n < 0
        return []
    end
    if n == 0
         return [[]]
    end
    all_changes = []

    for last_used_coin in coins
        combos = find_changes(n - last_used_coin, coins)
        for combo in combos
            combo.push(last_used_coin)
            if not all_changes.include?(combo.sort) then
              all_changes.push(combo.sort)
            end
        end
    end

    all_changes
end

def ver2changes(n, coins)
    ways = [0] * (n + 1)
    ways[0] = 1
    for coin in coins
        for j in (coin..n)
            ways[j] = ways[j] + ways[j - coin]
        end
    end
    return ways[n]
end
N = gets.to_i
puts ver2changes(N, [500,100,50,10,5,1])
