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
  A := int(0)
  B := int(0)
  fmt.Scan(&A)
  fmt.Scan(&B)
  for i := 0; i <= 200; i++ {
    for j := 0; j <= 200; j++ {
      a, b := float64(i), float64(j)
      if A == int(100*a/(a+b) + 0.5) && B == int(100*b/(a+b) + 0.5) {
        fmt.Println(i+j)
        return
      }
    }
  }
}
