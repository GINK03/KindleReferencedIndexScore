

puts gets.strip.split(" ").map { |x| x.to_i }.map { |x|  
  if x > 5 then 
    x = 5
  end
  x
}.inject { |a, x| a+x }

