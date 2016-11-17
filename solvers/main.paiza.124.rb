
line = (0..2).map { |x| gets.to_i }
a, b, c =  line
if a == b and b == c and c == a then 
  puts "YES"
else
  puts "NO"
end
