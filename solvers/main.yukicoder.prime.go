package main 

import ( 
  "fmt"
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
  fmt.Println(plist(100))
}
