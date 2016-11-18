package main

import (
  "bufio"
  "fmt"
  "os"
  "strconv"
  "strings"
  _ "math"
)

func main() {
  scanner := bufio.NewScanner(os.Stdin)
  hold := []int{}
  S := ""
  for scanner.Scan() {
   for i, t := range strings.Split(scanner.Text(), " " ) {
      if i == 0 {
        S = t
      } else {
        t_i, _ := strconv.Atoi(t)
        hold = append(hold, t_i)
      }
    }
    break
  }
  t, u := hold[0], hold[1]
  Ss := []rune(S)
  Ss[t] = 0
  Ss[u] = 0
  ReS := []rune{}
  for _, r := range Ss {
    if r != 0 {
      ReS = append(ReS, r)
    }
  }
  fmt.Println(string(ReS))
}

