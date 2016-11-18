package main 

import ( 
  "fmt"
	"bufio"
	"strconv"
	"os"
)
 
func plist(in int) []int {
	motos := []bool{}
	for i := 0; i <= in; i++ {
	  motos = append(motos, true)
	}

	i := 2
	for i*i <= in {
    if motos[i] {
      j := i*2
      for j <= in { 
         motos[j] = false
         j += i
      }
    }
    i += 1
	}
  
  res := []int{}
  for i := 2; i <= in; i++ {
    if motos[i] {
      res = append(res, i)
    }
  }
  return res
}

func main() {
	scanner := bufio.NewScanner(os.Stdin)
	N := 0
	for scanner.Scan() {
	  N, _ = strconv.Atoi(scanner.Text())
		break
	}
	ps := plist(10000000)
	ps[0] = 3
	ps[1] = 4
	for _, p := range ps {
	  if N % p == 0 {
		  fmt.Println(p)
			os.Exit(0)
		}
	}
	if N%2 == 0 {
	  fmt.Println(N / 2)
		os.Exit(0)
	}
	fmt.Println(N)
}
