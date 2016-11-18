
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
  srcs := []int{}
  scanner := bufio.NewScanner(os.Stdin)
  for scanner.Scan() {
    for _, x := range strings.Split(scanner.Text(), "/") {
      x2, _ := strconv.Atoi(x)
      srcs = append(srcs, x2)
    }
    if len(srcs) == 4 { break }
  }
  ax, ay, bx, by := srcs[0], srcs[1], srcs[2], srcs[3]
  head := ax*by + ay*bx
  tail := ay*by
  gcd := GCD(head, tail)
  if tail/gcd != 1 {
    fmt.Println(strconv.Itoa(head/gcd) + "/" + strconv.Itoa(tail/gcd))
  } else {
    fmt.Println(strconv.Itoa(head/gcd))
  }
}
//　GCDを再帰で計算します
func GCD(a, b int) int {
  if b == 0 {
    return a
  }
  return GCD(b, a%b)
}


