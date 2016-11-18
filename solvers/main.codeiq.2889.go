
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
    for _, x := range strings.Split(scanner.Text(), " ") {
      x2, _ := strconv.Atoi(x)
      srcs = append(srcs, x2)
    }
    break
  }
  // 等差数列かどうかチェックします
  next := append([]int{0}, srcs...)
  diffs := []int{}
  for i := 0; i < len(srcs); i++ {
    diffs = append(diffs, srcs[i] - next[i])
  }
  isA := true
  Ahead := diffs[1]
  for _, x := range diffs[1:] {
    if Ahead != x { 
      isA = false
    }
  }
  if isA {
    fmt.Println("A")
    return
  }
  // 等比数列かどうかチェックします
  // indexの一番目(0)は評価しようが無いので無視します
  remainds := []float64{}
  for i := 1; i < len(srcs); i++ {
    remainds = append(remainds, float64(next[i])/float64(srcs[i]) )
  }
  isG := true
  headG := remainds[0]
  for _, remaind := range remainds {
    if headG != remaind {
      isG = false
    }
  }
  if isG {
    fmt.Println("G")
    return
  }
  // fibonacci数列かどうかチェックします
  // indexの一番目と２番めは評価しようがないので無視します ignore index 0, 1
  isFibonacci := true
  for i := 2; i < len(srcs); i++ {
    if ( srcs[i] != srcs[i - 1] + srcs[i - 2] ) {
      isFibonacci = false
    }
  }
  if isFibonacci {
    fmt.Println("F")
    return  
  }

  fmt.Println("x")
}
//　GCDを再帰で計算します
func GCD(a, b int) int {
  if b == 0 {
    return a
  }
  return GCD(b, a%b)
}


