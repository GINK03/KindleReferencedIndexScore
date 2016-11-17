

def calc(m, v)
  r = v % (2 * m) 
  r < m ? r : 2 * m - 1 - r
end

def run
  n, m = gets.strip.split(" ").map { |x| x.to_i }
  xx, yy = gets.strip.split(" ").map { |x| x.to_i }
  puts calc(m, xx-1) == calc(m, yy-1) ? 'YES' : 'NO'
end 

class D
  @i = 0
  @c = 0
  def initialize
  end
  attr_accessor :i
  attr_accessor :c
end
def mark0
  # 上がったり下がったりするロジック
  data = []
  (0..m-1).map {|x| x.to_i }.each_with_index {|i, x|
    c = i % n
    d = D.new
    d.i = x+1
    if (i/n).to_i%2 == 0 then
      d.c = c
    else
      d.c = n - c - 1
    end
    data.push(d)
  }

  xsan = data.select {|x| x.i == xx}.first
  ysan = data.select {|x| x.i == yy}.first
  if xsan.c == ysan.c then 
    puts "YES"
  else 
    puts "NO"
  end
end 

run()
