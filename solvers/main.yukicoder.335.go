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
	holder := []int{}
	th := 0
	for scanner.Scan() {
	  th += 1
		for _, t := range strings.Split(scanner.Text(), " ") { 
			x3, _ := strconv.Atoi(t) 
			holder = append(holder, x3)
		}
		if th == 1 { break }
	}
	A, B := holder[0], holder[1]

	if A < B {
	  fmt.Println(B - 1 - 1)
	} else if A > B {
	  fmt.Println(2000000000 - B - 1)
	}
}
