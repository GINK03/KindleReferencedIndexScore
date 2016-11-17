
(0..2).map { |x| 
  gets.strip
}.zip(["Gold", "Silver", "Bronze"]).map{ |x, y| 
  puts y + " " + x
}
