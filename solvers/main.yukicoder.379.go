package main

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
	"strings"
	_ "math"
	_ "sort"
)


func main() {
	scanner := bufio.NewScanner(os.Stdin)
	th := 0
	tgt := []float64{}
	for scanner.Scan() {
	  th += 1
		text := scanner.Text()
		if text == "" { break }
		for _, t := range strings.Split(text, " ") {
		  n, _ := strconv.ParseFloat(t, 64) 
		  tgt = append(tgt, n)
	  }
		if th == 1 { break }
	}
	money, bamount, length := tgt[0], tgt[1], tgt[2]
	total := (float64(int(money)/5) * bamount) / length

	//fmt.Println(money, bamount, length)
	fmt.Printf("%9.18f", total)
	fmt.Println()
}
