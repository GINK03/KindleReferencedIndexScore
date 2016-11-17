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
	fmt.Println(316 - 52 + 52*N)
}

