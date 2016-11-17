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
	holder := []int{}
	th := 0
	for scanner.Scan() {
	  th += 1
		x3, _ := strconv.Atoi(scanner.Text()) 
		holder = append(holder, x3)
		if th == 1 { break }
	}
  N := holder[0]
	znum := 0
	znum = (N/3 + N/5)*2
	fmt.Println(znum)
}

