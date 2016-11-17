
package main

import (
  "bufio"
  "fmt"
  "os"
  "strconv"
  "strings"
  _ "math"
  "sort"
)

func main() {
  srcs := []float64{}
  _ = gets()
  for _, x := range strings.Split(gets(), " ") {
    x2, _ := strconv.ParseFloat(x, 64)
    srcs = append(srcs, x2)
  }
  sort.Float64s(srcs)
  if len(srcs) % 2 == 0 {
    mid := len(srcs)/2
    fmt.Println( (srcs[mid-1] + srcs[mid])/2.0 )
  } else {
    mid := len(srcs)/2
    fmt.Println( srcs[mid] )
  }
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
