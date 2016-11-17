
buff = { "strike" => 0, "ball" => 0 }
N = gets.to_i
(1..N).map { |x| 
  cat = gets.strip
  buff[cat] += 1
  if cat == "strike" and buff[cat] == 3 then 
    puts "out!"
  end
  if cat == "strike" and buff[cat] < 3 then
    puts "strike!"
  end
  if cat == "ball" and buff[cat] == 4 then
    puts "fourball!"
  end
  if cat == "ball" and buff[cat] < 4 then
    puts "ball!"
  end
}
