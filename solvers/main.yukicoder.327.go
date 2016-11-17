package main

import (
  _ "bufio"
  "fmt"
  _ "os"
  _ "strconv"
  _ "strings"
  _ "math"
  _ "sort"
)

func main() {
  N := 0
  fmt.Scan(&N)
  runes := []rune{}
  for true {
    runes = append(runes, rune(N%26 + 65) )
    N /= 26
    if N <= 0 { break }
    // このNを一個引く作業がすごく重要🌟 　気付かずにわけわかんない試行錯誤することになった
    N--
  }
  res := string(runes)
  fmt.Println(Reverse(res))
}

func Reverse(s string) string {
  runes := []rune(s)
  for i, j := 0, len(runes)-1; i < j; i, j = i+1, j-1 {
    runes[i], runes[j] = runes[j], runes[i]
  }
  return string(runes)
}


