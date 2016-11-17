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
  ok := false
  i := 0
	for i <= 999 {
    fmt.Printf("%03d", i)
    fmt.Println()
    for scanner.Scan() {
      if scanner.Text() == "unlocked" { ok = true }
      break
    }
    if ok { break }
    i += 1
  }
}

