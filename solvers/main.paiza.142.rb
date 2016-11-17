
ins = (0..4).map{ |x| 
  gets.to_i
}
puts (1..ins.length-1).map{ |i|
  ins[i] - ins[i-1]
}
