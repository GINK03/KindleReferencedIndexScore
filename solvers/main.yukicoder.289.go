package main

import (
  "bufio"
  "fmt"
  "os"
  _ "strconv"
  _ "strings"
  _ "math"
)

func main() {
  scanner := bufio.NewScanner(os.Stdin)
  hold := []rune{}
  for scanner.Scan() {
    for _, r := range scanner.Text() {
      if 48 <= r && r <= 57 {
        hold = append(hold, r)
      }
    }
    break
  }
  sum := 0
  for _, r := range hold {
    sum += int(r - 48)
  }
  fmt.Println(sum)
}

