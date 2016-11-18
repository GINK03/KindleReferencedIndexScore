package main

import (
  "bufio"
  "fmt"
  "os"
  "sort"
  _ "strconv"
  _ "strings"
  _ "math"
)

func main() {
  scanner := bufio.NewScanner(os.Stdin)
  hold_t := []rune{}
  hold_r := []rune{}
  hold_e := []rune{}
  for scanner.Scan() {
    for _, r := range scanner.Text() {
      if r == rune(116) {
        hold_t = append(hold_t, r)
      }
      if r == rune(114) {
        hold_r = append(hold_r, r)
      }
      if r == rune(101) {
        hold_e = append(hold_e, r)
      }
    }
    break
  }

  may_ans := []int{len(hold_t), len(hold_r), len(hold_e)/2}
  sort.Ints(may_ans)
  fmt.Println(may_ans[0])
}

