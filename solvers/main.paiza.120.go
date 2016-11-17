
package main

import (
  "bufio"
  "fmt"
  "os"
  _ "strconv"
  _ "strings"
  _ "math"
  _ "sort"
)

func main() {
  a, b := 0, 0
  fmt.Scan(&a)
  fmt.Scan(&b)
  if b%a != 0 {
    fmt.Println( b/a + 1 )
  } else {
    fmt.Println( b/a )
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
