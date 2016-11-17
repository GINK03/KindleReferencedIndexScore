package main

import (
  "bufio"
  "fmt"
  "os"
  _ "sort"
  "strconv"
  _ "strings"
  _ "math"
)

func main() {
  scanner := bufio.NewScanner(os.Stdin)
  Price := float64(0)
  for scanner.Scan() {
    Price, _ = strconv.ParseFloat(scanner.Text(), 64)
    break
  }
  fmt.Printf("%9.2f", Price*1.08)
  fmt.Println()
}

