package main

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
	"strings"
	_ "math"
	"sort"
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
	sort.Float64s(tgt)
	next := make([]float64, len(tgt))
	copy(next, tgt)
	next = next[1:len(next)-1]
	sum := 0.
	for _, n := range next {
	  sum += n
	}
	fmt.Printf("%2.2f", sum/float64(len(next)) )
	fmt.Println()
	//fmt.Println(next)
}
