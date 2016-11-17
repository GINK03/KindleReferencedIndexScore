
a, b, c = gets.split(" ").map { |x| x.to_i } 
if a < b*c then
  puts "OK"
else
  puts "NG"
end
