
dx = [-2,-2,-1,-1,1,1,2,2]
dy = [-1,1,-2,2,-2,2,-1,1]

conbi = (dx.zip(dy).map {|x, y|
  [x,y]
} * 3 ).combination(3).map { |x|
  x
} + (dx.zip(dy).map {|x, y|
   [x,y]
} * 2 ).combination(2).map { |x| 
   x
} + (dx.zip(dy).map {|x, y|
    [x,y]
} * 1 ).combination(1).map { |x|  
    x
}

conbix = conbi.map{ |x|
  x.map { |x| x[0] }.inject { |a,x| a+x }
}
conbiy = conbi.map{ |x|
  x.map { |x| x[1] }.inject { |a,x| a+x }
}

reduced = conbix.zip(conbiy)
reduced.push([0,0])

x, y = gets.split(" ").map { |x| x.to_i } 
if reduced.include?([x,y]) then 
  puts "YES"
else
  puts "NO"
end
