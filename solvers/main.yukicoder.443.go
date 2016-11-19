package main

import (
	"bufio"
	"fmt"
	"math/big"
	"os"
)

func Iter(p []rune) func() int {
	f := pf(len(p))
	return func() int {
		return f(p)
	}
}

// Recursive function used by perm, returns a chain of closures that
// implement a loopless recursive SJT.
func pf(n int) func([]rune) int {
	sign := 1
	switch n {
	case 0, 1:
		return func([]rune) (s int) {
			s = sign
			sign = 0
			return
		}
	default:
		p0 := pf(n - 1)
		i := n
		var d int
		return func(p []rune) int {
			switch {
			case sign == 0:
			case i == n:
				i--
				sign = p0(p[:i])
				d = -1
			case i == 0:
				i++
				sign *= p0(p[1:])
				d = 1
				if sign == 0 {
					p[0], p[1] = p[1], p[0]
				}
			default:
				p[i], p[i-1] = p[i-1], p[i]
				sign = -sign
				i += d
			}
			return sign
		}
	}
}

func main() {
	scanner := bufio.NewScanner(os.Stdin)
	th := 0
	lines := []string{}
	for scanner.Scan() {
		th += 1
		text := scanner.Text()
		lines = append(lines, text)
		if th == 1 {
			break
		}
	}
	target := lines[0]
	set := make(map[rune]struct{})
	runes := []rune(target)
	for _, r := range runes {
		set[r] = struct{}{}
	}
	setl := []rune{}
	for r := range set {
		setl = append(setl, r)
	}
	fmt.Println(string(setl))
	runes = []rune(setl)
	i := Iter(runes)
	ns := []big.Int{}
	for sign := i(); sign != 0; sign = i() {
		//fmt.Println(string(runes))
		n := *big.NewInt(0)
		n.SetString(string(runes), 10)
		ns = append(ns, n)
	}
	n_tmp := ns[0]
	for _, n_adhoc := range ns {
		n_tmp.GCD(nil, nil, &n_tmp, &n_adhoc)
	}
	fmt.Println(&n_tmp)
}
