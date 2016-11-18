
def evals() 
  # Go言語のヴァージョンが古く、動作がおかしいようです。
  # 何度も提出してしまい、申し訳ありませんでした 
  srcs = gets.strip!.split(" ").map{|x| 
   x.to_i
  }
  nexts = srcs.dup
  nexts.insert(0, 0) 
  deltas = srcs.zip(nexts).map { |x, y|
    x - y
  }.slice(1..srcs.length)
  if deltas.all?{ |x| x == deltas[0] } then
    puts "A"
    return
  end
  
  isF = (2..srcs.length-1).map { |i|
    srcs[i] == srcs[i - 1] + srcs[i -2]
  }.all? { |x| x}
  # フィボナッチ数列は5ω2 + 4か 5w2 - 4 が完全スクエア型になることが条件らしいです
  really = ((5*srcs[0]**2 - 4)**0.5).to_i ** 2 == 5*srcs[0]**2 - 4 || ((5*srcs[0]**2 + 4)**0.5).to_i ** 2 == 5*srcs[0]**2 + 4

  if isF and really then
    puts "F"
    return 
  end

  rels = srcs.zip(nexts).map { |x, y| 
    res = 'infinit'
    if y != 0 then
      res = x.to_f / y.to_f
    end
    res
  }.slice(1..srcs.length)
  k = rels[0]
  recovers = (0..srcs .length-1).map { |i| 
    (srcs[0]*(k**i)).to_i
  }
  if rels.all? { |x| x == rels[0] } then
   puts "G"
   return
  end
  
  puts "x"
end

evals()
