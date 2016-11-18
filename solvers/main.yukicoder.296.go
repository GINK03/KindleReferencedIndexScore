package main

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
	"strings"
	_ "math"
)

func main() {
  scanner := bufio.NewScanner(os.Stdin)
	hold := []int{}
	for scanner.Scan() {
	 for _, t := range strings.Split(scanner.Text(), " " ) {
		  t_i, _ := strconv.Atoi(t)
			hold = append(hold, t_i)
		}
    break
  }
	N, H, M, T := hold[0], hold[1], hold[2], hold[3]
	Mtotal := 60 * H + M
	OverSleepTime := (N - 1)*T
	Mtotal += OverSleepTime
	fmt.Println( (Mtotal/60)%24 )
	fmt.Println(Mtotal%60)
}

