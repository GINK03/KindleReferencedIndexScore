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
	holder := [][]float64{}
	th := 0
	for scanner.Scan() {
	  th += 1
	  pair := []float64{}
		text := scanner.Text()
		if text == "" { break }
	  for i, x2 := range strings.Split(text, " ") {
			x3, e := strconv.ParseFloat(x2, 64)
			_ = e
			_ = i
			pair = append(pair, x3)
		}
		holder = append(holder, pair)
		if th == 2 { break }
	}
	x, y := math.Abs(holder[0][0] - holder[1][0]), math.Abs(holder[0][1] - holder[1][1])
	//distance := math.Sqrt( math.Pow((holder[0][0] - holder[1][0]),2) + math.Pow((holder[0][1] - holder[1][1]),2) )/2
	//fmt.Println(holder)
	fmt.Println( (x + y)/2 )
	//fmt.Println(distance)
}
