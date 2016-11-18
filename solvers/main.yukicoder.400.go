package main

import (
	"bufio"
	"fmt"
	"os"
	_ "strconv"
	_ "strings"
	_ "math"
	_ "sort"
)

func Reverse(s []rune) []rune {
  runes := s
  for i, j := 0, len(runes)-1; i < j; i, j = i+1, j-1 {
		runes[i], runes[j] = runes[j], runes[i]
	}
	return runes
}

func main() {
	scanner := bufio.NewScanner(os.Stdin)
	holder := []rune{}
	th := 0
	for scanner.Scan() {
	  th += 1
		text := scanner.Text()
		if text == "" { break }
	  for i, x2 := range text {
		   _ = i
		   holder = append(holder, x2)
		}
		if th == 1 { break }
	}
	holder = Reverse(holder)
	result_runes := []rune{}
	for _, r := range holder {
	  if string(r) == ">" {
		  result_runes = append(result_runes, []rune("<")[0])
		}
		if string(r) == "<" {
		  result_runes = append(result_runes, []rune(">")[0])
		}
	}
	fmt.Println(string(result_runes))
}
