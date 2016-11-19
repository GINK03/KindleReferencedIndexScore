package main

import (
	"bufio"
	"fmt"
	_ "math"
	_ "math/big"
	"os"
	_ "reflect"
	"regexp"
	"strconv"
	_ "strings"
)

func main() {
	scanner := bufio.NewScanner(os.Stdin)
	th := 0
	lines := []string{}
	for scanner.Scan() {
		th += 1
		text := scanner.Text()
		lines = append(lines, text)
		if th == 2 {
			break
		}
	}
	a, ae := strconv.ParseInt(lines[0], 10, 64)
	b, be := strconv.ParseInt(lines[1], 10, 64)
	if ae != nil || be != nil || a > 12345 || b > 12345 || (len(lines[0]) > 1 && regexp.MustCompile(`^0{1,}`).MatchString(lines[0])) || (len(lines[1]) > 1 && regexp.MustCompile(`^0{1,}`).MatchString(lines[1])) {
		fmt.Println("NG")
	} else {
		fmt.Println("OK")
	}
}
