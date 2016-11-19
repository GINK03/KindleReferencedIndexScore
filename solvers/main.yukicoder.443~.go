package main

import (
	"bufio"
	"fmt"
	"math/big"
	"os"
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
	//d := []rune{}
	g := big.NewInt(0)
	g.SetString(text, 10)

	set := make(map[rune]struct{})
	for _, r := range []rune(text) {
		set[r] = struct{}{}
	}
	setl := []rune{}
	for r := range set {
		setl = append(setl, r)
	}
	for _, x := range setl {
		for _, y := range setl {
			if x == y {
				continue
			}
			bx, by, t := big.NewInt(0), big.NewInt(0), big.NewInt(0)
			bx.SetString(string(x), 10)
			by.SetString(string(y), 10)
			t = new(big.Int).Mul(big.NewInt(9), new(big.Int).Abs(new(big.Int).Sub(bx, by)))
			//fmt.Println("a", t, bx, by)
			g.GCD(nil, nil, t, g)
		}
	}
	fmt.Println(g)
}
