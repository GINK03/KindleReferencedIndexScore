
package main

import (
  "bufio"
  "fmt"
  "os"
  _ "strconv"
  "strings"
  _ "math"
  _ "sort"
)

func main() {
  a, b := "", ""
  fmt.Scan(&a)
  fmt.Scan(&b)
  fmt.Println(strings.Join([]string{a, "@", b}, "") )
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
