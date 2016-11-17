package main

import (
	"bufio"
	"fmt"
	_ "math"
	"math/big"
	"os"
	_ "strconv"
	"strings"
)

func main() {
	scanner := bufio.NewScanner(os.Stdin)
	holder := []big.Int{}
	th := 0
	for scanner.Scan() {
		th += 1
		text := scanner.Text()
		for _, x2 := range strings.Split(text, " ") {
			bigint := *big.NewInt(0)
			bigint.SetString(x2, 10)
			holder = append(holder, bigint)
		}
		if th == 1 {
			break
		}
	}
	a, b := holder[0], holder[1]
	//fmt.Printf("a %v\n", &a)
	//fmt.Printf("b %v\n", &b)
	op1 := big.NewInt(0)
	op2 := big.NewInt(0)
	op1.Add(&a, &b)
	op2.Mul(&a, &b)
	//fmt.Printf("cmp %v\n", add.Cmp(mul))
	//fmt.Printf("add %v\n", add)
	//fmt.Printf("mul %v\n", mul)

	if op1.Cmp(op2) == 1 {
		fmt.Printf("S")
		fmt.Println()
	} else if op1.Cmp(op2) == -1 {
		fmt.Printf("P")
		fmt.Println()
	} else {
		fmt.Printf("E")
		fmt.Println()
	}
}
