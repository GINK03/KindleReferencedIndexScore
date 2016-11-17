package main

import (
  "bufio"
  "fmt"
  "os"
  "strconv"
  _ "strings"
  _ "math"
  "sort"
)

func main() {
  scanner := bufio.NewScanner(os.Stdin)
  holder := []int{}
  th := 0
  Max := 0
  for scanner.Scan() {
    x,  _ := strconv.Atoi(scanner.Text()) 
    holder = append(holder, x)
    if th == 0 {
      Max = x
    }
    if th == Max { break } 
    th += 1
  }
  nums := holder[1:]
  sort.Ints(nums)
  
  for prime := 100; prime >= 2; prime-- {
    acc := 0
    for _, n := range nums {
      acc += n % prime
    }
    if acc == 0 {
      for i, _ := range nums {
        nums[i] /= prime
      }
    }
  }
  acc := 0
  for _, val := range nums {
    acc += val
  }
  fmt.Println(acc)
}
