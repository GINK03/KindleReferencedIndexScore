package main

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
	_ "strings"
	_ "math"
	_ "sort"
)


func main() {
	scanner := bufio.NewScanner(os.Stdin)
	th := 0
	tgt := ""
	for scanner.Scan() {
	  th += 1
		text := scanner.Text()
		if text == "" { break }
		tgt = text
		if th == 1 { break }
	}
  tgti, _ := strconv.Atoi(tgt)  
	if tgti >  43 {
	  fmt.Println(tgti - 7)
		os.Exit(0)
	}

	all := [][]int{}
	for i := 2; i < 100; i++ {
	  r, e := strconv.ParseInt("17", i, 32)
		_ = e
		_ = r
		if e == nil {
			all = append(all, []int{ int(r), i } )
	  }
	  //fmt.Println(i, " ",r," ",  e)
	}
	for _, a := range all {
	  if a[0] == tgti {
		  fmt.Println(a[1])
			os.Exit(0)
		}
	}
	fmt.Println(-1)
	//fmt.Println("max ", all[len(all)])
}
