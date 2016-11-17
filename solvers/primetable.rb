def prime_table(n)
  plist = (0..n).map { |x| true }
  i = 2
  while i * i <= n do
    if plist[i] then
      j = i + i
      while j <= n do
        plist[j] = false
        j += i
      end
    end
    i += 1
  end

  table = (2..plist.length-1).map { |i| 
    if plist[i] then
      i
    else 
      nil
    end
  }.select { |x| x != nil }
  return table
end

pt = prime_table(50)
p pt
p "1"*(pt.length)

max = ("1"*pt.length). to_i(2)
p (0..max).map { |x| 
  x.to_s(2).split(//).map { |x2| x2.to_i }.zip(pt).map { |i, x3| 
    i*x3
  }.inject{|a,s| a+s}
}
