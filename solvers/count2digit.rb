

N, M = gets.split(" ").map { |x| x.to_i } 

base = ("1"*M).to_i(2)
if base > N then
  puts 0
  exit(0)
end
count = 0
(base..N).map{ |i|
  if M == i.to_s(2).count("1") then 
    count += 1
  end  
}
puts count
