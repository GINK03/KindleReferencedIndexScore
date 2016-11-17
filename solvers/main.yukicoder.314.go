package main

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
	_ "strings"
	_ "math"
)

func main() {
  scanner := bufio.NewScanner(os.Stdin)
	N := 0
	for scanner.Scan() {
	  N, _ = strconv.Atoi(scanner.Text())
    break
  }
	Ps := []int{1,2}
	for i := 3; i <= N; i++ {
	  rng := i - 1
	  Pnext := Ps[rng - 1] + Ps[rng - 2] - 1
		Ps = append(Ps, Pnext)
	}
	fmt.Println(Ps)
}

