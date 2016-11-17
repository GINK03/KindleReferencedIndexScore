
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
  a := ""
	var base rune
	base = []rune("A")[0] - 1
  fmt.Scan(&a)
  fmt.Println( []rune(a)[0] - base )
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
