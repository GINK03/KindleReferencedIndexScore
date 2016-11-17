package main

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
	"strings"
	"math"
)

func main() {
	scanner := bufio.NewScanner(os.Stdin)
	holder := []float64{}
	th := 0
	for scanner.Scan() {
	  th += 1
		text := scanner.Text()
	  for _, x2 := range strings.Split(text, " ") {
			x3, e := strconv.ParseFloat(x2, 64)
			_ = e
			holder = append(holder, x3)
		}
		if th == 1 { break }
	}
	a, b := holder[0], holder[1]
	if a != b {
	  fmt.Printf("%10.20f", math.Pow(math.Abs(math.Pow(a, 2) - math.Pow(b, 2)), 0.5) )
	  fmt.Println()
  }else {
	  fmt.Printf("%10.20f", math.Pow(math.Abs(math.Pow(a, 2) +  math.Pow(b, 2)), 0.5) )
	  fmt.Println()
	}
}
