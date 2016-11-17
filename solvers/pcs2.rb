
N = gets.to_i 
seeds = []

def ncr(n, r)
  a, b = r, n-r
  a, b = b, a if a < b  # a is the larger
  numer = (a+1..n).inject(1) { |t,v| t*v }  # n!/r!
  denom = (2..b).inject(1) { |t,v| t*v }    # (n-r)!
  numer/denom
end
for x in (0..N) 
  if x == 0 then 
     seeds.push(1)
  elsif x == 1 then
     seeds.push(0)
  elsif x == 2 then 
     seeds.push(1)
  elsif x == 3 then
     seeds.push(2)
  else 
     ncrs = (1..x).to_a.sort {|a, b| b <=> a }.map { |x2| 
       [x, x2]
     }.map { |x3| 
       ncr(x3[0], x3[1])
     }
     sum_ = ncrs.zip(seeds).map{ |x2| 
       x2[0] * x2[1]
     }.inject{ |sum, x2| 
       sum + x2
     }
     next_ = (1..x).inject{ |conv, x2|
       conv * x2
     } - sum_
     seeds.push(next_)
  end
end
p seeds.pop
