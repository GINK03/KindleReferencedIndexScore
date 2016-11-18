package main

import (
	"bufio"
	"fmt"
	"os"
	_ "strconv"
	_ "strings"
	_ "math"
)

func main() {
	scanner := bufio.NewScanner(os.Stdin)
	th := 0
	for scanner.Scan() {
	  th += 1
		text := scanner.Text()
		_ = text
		fmt.Println("Hello World!")
		if th == 1 { break }
	}
	//x, y := math.Abs(holder[0][0] - holder[1][0]), math.Abs(holder[0][1] - holder[1][1])
	//fmt.Println( (x + y)/2 )
}
