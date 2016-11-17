require 'prime'
n = gets.to_i.prime_division
ans = n.map { |x| x[0]*(x[1]%2) }.select {|x| x > 0 }.inject { |a,x| a*x }
if ans == nil then 
  puts "1"
else 
  puts ans
end
