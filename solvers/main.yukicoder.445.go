package main

import (
	"bufio"
	"fmt"
	_ "math"
	_ "math/big"
	"os"
	"strconv"
	"strings"
)

func main() {
	scanner := bufio.NewScanner(os.Stdin)
	th := 0
	var a, b float64
	for scanner.Scan() {
		th += 1
		text := scanner.Text()
		x2 := strings.Split(text, " ")
		a, _ = strconv.ParseFloat(x2[0], 64)
		b, _ = strconv.ParseFloat(x2[1], 64)
		if th == 1 {
			break
		}
	}
	fmt.Println(int64(50.0*a + (50.0 * a / (0.8 + 0.2*b))))
}
