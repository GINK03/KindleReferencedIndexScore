package main
import (
  "fmt"
  "os"
  "bufio"
 )


func main() {
  in_s := gets()
  in_r := []rune(in_s)
  ans_sum := 0
  w_num := 0
  for i := len(in_r) -1; i >= 0; i-- {
    if in_r[i] == []rune("w")[0] { 
      w_num += 1
    }
    if in_r[i] == []rune("c")[0] {
      // Cまでの位置で、Wが何回出るかをカウントして、出た数のnC2だけ組み合わせがある。それを累積する
      ans_sum += w_num * (w_num - 1)/2
    }
  }
  fmt.Println(ans_sum)
}


var rdr = bufio.NewReaderSize(os.Stdin, 10000000)
func gets() string {
  buf := make([]byte, 0, 10000000)
  for {
    l, p, _ := rdr.ReadLine()
    buf = append(buf, l...)
    if !p { break }
  }
  return string(buf)
}
