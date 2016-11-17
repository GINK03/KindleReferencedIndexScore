h = {
 "A" => "4",
 "E" => "3",
 "G" => "6",
 "I" => "1",
 "O" => "0",
 "S" => "5",
 "Z" => "2"
}

puts gets.strip.split(//).map { |x| 
  if h.has_key?(x) then 
    h[x]
  else
    x
  end
}.join("")
