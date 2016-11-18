
t2x = [[]]

n = gets.to_i

inv = 1.upto(n).map { |x| 
  gets.split(" ").map { |x2| 
    res = 0
    if x2 == "nyanpass" then
      res = 1
    else
      res = 0
    end
    res 
  }
}
heads = (0..n-1).map {|x|  
  inv.map { |i| 
    i[x]
  }.inject {|a,s| a+s} 
}.map.with_index { |o, i| 
  [i+1, o]
}.map { |x| x} .sort { |a,b| b[1] <=> a[1] }

head = heads.first
seco = heads[1]
if head[1] == n-1 and head[1] != 0 and head[1] != seco[1] then 
  puts head[0]
else 
  puts "-1"
end

