package main

import (
	"bufio"
	"fmt"
	_ "math"
	_ "math/big"
	"os"
	_ "strconv"
	_ "strings"
)

var rdr = bufio.NewReaderSize(os.Stdin, 10000000)

func gets() string {
	buf := make([]byte, 0, 10000000)
	for {
		l, p, _ := rdr.ReadLine()
		buf = append(buf, l...)
		if !p {
			break
		}
	}
	return string(buf)
}
func main() {
	text := gets()
	c := 0
	w := 0
	for _, ch := range text {
		if string(ch) == "c" {
			c += 1
		}
		if string(ch) == "w" {
			w += 1
		}
	}
	if c-1 > w {
		fmt.Println(w)
	} else {
		fmt.Println(c - 1)
	}
}
