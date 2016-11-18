
package main

import (
  "bufio"
  "fmt"
  "os"
  _ "strconv"
  _ "strings"
  _ "math"
  "sort"
)

func main() {
	N, M := 0, 0
	fmt.Scan(&N, &M)
	fmt.Println(N, M)
	pos := []int{}
  for i := 0; i < M; i++  {
	  p := 0
		fmt.Scan(&p)
    pos = append(pos, p)
  }
	sort.Ints(pos)
	ans := 9999999999999.9
	for i := 0; i <= M-N+1; i++ {
	  fmt.Println(i)
		left, right = pos[i], pos[i+N
	}
	fmt.Println(ans)
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
