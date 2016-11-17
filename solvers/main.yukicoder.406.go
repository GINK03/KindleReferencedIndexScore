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
	holder := []int{}
	th := 0
	Num := 0
	for scanner.Scan() {
	  fmt.Println(scanner.Text())
	}
	os.Exit(0)
	for scanner.Scan() {
	  th += 1
		text := scanner.Text()
		fmt.Println(text)
		
		if th == 1 {
		  Num, _ = strconv.Atoi(text)
		}
		_ = Num
		if th == 2 {
			for i, x2 := range strings.Split(text, " ") {
				x3, e := strconv.Atoi(x2)
				_ = e
				_ = i
				holder = append(holder, x3)
			}
	 	}
		if th == 2 { break }
	}
	sort.Ints(holder)
  dholder := make([]int, len(holder))
	copy(dholder, holder)
	dholder = append([]int{0}, dholder...)

	next := []int{}
	for i, ent := range holder {
	  _ = ent
		next = append(next, []int{ holder[i] - dholder[i]}... )
	}
	/*fmt.Println(holder)
	fmt.Println(dholder)
	fmt.Println(next)*/
	next = next[1:]
	fmt.Println(next)
	tgt := next[1]
	for _, ent :=  range next {
	    if tgt != ent || tgt == 0 {
		    fmt.Println("NO")
			  os.Exit(0)
		  }
	}
	fmt.Println("YES")
}
