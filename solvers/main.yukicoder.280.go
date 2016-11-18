package main

import (
  "bufio"
  "fmt"
  "os"
  _ "sort"
  "strconv"
  "strings"
  _ "math"
)

func main() {
  scanner := bufio.NewScanner(os.Stdin)
  ins := []string{}
  for scanner.Scan() {
    ins = append(ins, scanner.Text() )
    if len(ins) == 2 { break }
  }
  Hnums := []int{}
  for _, hnum := range strings.Split(ins[1]," ") {
     hnum_i, _ := strconv.Atoi(hnum)
     Hnums = append(Hnums, hnum_i)
  }
  head := strconv.Itoa(Hnums[0])
  tail := strconv.Itoa(Hnums[len(Hnums) - 1])
  fmt.Println(tail + "/" + head)
}

