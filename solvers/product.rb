

a,b = gets.split(" ")
len = a.to_i
blks= b.split("").to_a.repeated_permutation(len).collect { |x| x.join }.map { |x| 
  x.to_i
}.sort

print blks

if blks.length % 2 == 1 then
  mid_pos = [(blks.length / 2).to_i] 
else
  mid_pos = [(blks.length / 2).to_i-1, (blks.length / 2).to_i]
end
puts mid_pos.map { |x| 
  blks[x]
}.join(",")
