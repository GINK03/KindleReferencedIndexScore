

while line = STDIN.gets
  line = line.tr('０-９ａ-ｚＡ-Ｚ', '0-9a-zA-Z')
  line = line.gsub('％', '%')
  line = line.gsub(/\d{1,}/, 'number')
  line = line.downcase
  puts line
end
