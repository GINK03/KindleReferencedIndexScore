swap = {
  0 => 5,
  1 => 3,
  2 => 2,
  3 => 1
}

buff = { 0 => 0, 1 => 0, 2 => 0, 3=>0 }
N = gets.to_i
(1..N).map { |x| 
  cat, price  = gets.split(" ").map { |x2| x2.to_i }
  buff[cat] += price
}
puts buff.map{ |k, v| 
  (v/100) *swap[k]
}.inject { |acc, x| acc + x }
