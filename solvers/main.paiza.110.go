
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
  a, b := "", ""
  fmt.Scan(&a)
  fmt.Scan(&b)
  h, t := []rune(a)[0], []rune(b)[0]
  fmt.Println( string([]rune{h, []rune(".")[0], t}) )
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
