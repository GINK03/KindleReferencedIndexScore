package main 

import ( 
  "fmt"
)
 
func GCDRemainderRecursive(a, b int) int {
  if b == 0 {
    return a
  }
  return GCDRemainderRecursive(b, a%b)
}

func main() {
  N := 0
  fmt.Scan(&N)
  acc := 0
  for i := 0; i <= N; i++ {
    acc += i
  }
  fmt.Println(GCDRemainderRecursive(acc, N))
}
