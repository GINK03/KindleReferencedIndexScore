
line = gets.chomp(" ").chomp.gsub(/\s{1,}/, "\s").gsub(/\s,/, ",").gsub(/^\s/, "").gsub(/\s$/, "").gsub(/\s\./, ".").gsub(/\s!/, "!").gsub(/\s\?/, "?")
puts line

