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
	tgt := []int{}
	for scanner.Scan() {
	  th += 1
		text := scanner.Text()
		if text == "" { break }
		for _, t := range strings.Split(text, " ") {
		  n, _ := strconv.Atoi(t) 
		  tgt = append(tgt, n)
	  }
		if th == 1 { break }
	}
	head, tail := tgt[0], tgt[1]
	//fmt.Println(head, tail)
	delta := tail - head
	if delta == 0 {
	  fmt.Println(delta)
	}else if delta > 0 {
	  fmt.Println("+" + strconv.Itoa(delta))
	}else {
	  fmt.Println(delta)
	}
}
