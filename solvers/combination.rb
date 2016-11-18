

N = gets.to_i
ents = gets.split(" ").to_a.map {|x| x.to_i }
sums = []
ents.combination(2) { |x1, x2| 
  sums.push(x1+x2)
}
p sums
if sums.include?(256) then
  puts "yes"
else
  puts "no"
end
