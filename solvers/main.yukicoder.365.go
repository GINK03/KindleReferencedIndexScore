package main

import (
  "bufio"
  "fmt"
  "os"
  "strconv"
  "strings"
  _ "math"
  _ "sort"
)


func main() {
  //scanner := bufio.NewScanner(os.Stdin)
  N := 0
  fmt.Scan(&N)
  srcs := []int{}
  for _, x := range strings.Split(gets(), " ") {
    x2, _ := strconv.Atoi(x)
    srcs = append(srcs, x2)
  }
  diff := 0
  for i := len(srcs) - 1; i >= 0; i-- {
    if srcs[i] == N - diff {
      diff += 1
    }
  }
  fmt.Println(N - diff)
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
