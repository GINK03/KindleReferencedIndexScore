package main

import (
 "fmt"
)

func main() {
  src, tgt := "",""
  fmt.Scan(&src, &tgt)
  if len(src) > len(tgt) {
    fmt.Println(src)
    return 
  } else if len(src) < len(tgt) {
    fmt.Println(tgt)
    return
  }
  for i := 0; i < len(src) ; i++ {
    if src[i] == tgt[i] {
      continue
    }
    if src[i] == '7' && tgt[i] == '4' {
      fmt.Println(tgt)
      return
    } else if src[i] == '4' && tgt[i] == '7' {
      fmt.Println(src)
      return
    } else if src[i] < tgt[i] {
      fmt.Println(tgt)
      return
    } else {
      fmt.Println(src)
      return 
    }
  }

}
