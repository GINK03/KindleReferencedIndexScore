
n = gets.to_i
arr = (1..n).to_a


count = 0
arr.permutation(n).map { |x|
  x
}.map { |x|
  x = x.zip(arr)
  if x.select { |x1| 
    x1[0] == x1[1]
  }.length == 0 then
    count += 1
  end 
}
p count
