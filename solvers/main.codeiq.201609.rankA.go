
package main

import (
  "bufio"
  "fmt"
  "os"
  _ "strconv"
  _ "strings"
  _ "math"
  _ "sort"
)
type Vector struct {
  vector  []string
  checked bool
	cost    int
	block   string
}

func main() {
  n, m := 0, 0
	fmt.Scan(&n, &m)
  scanner := bufio.NewScanner(os.Stdin)
	yx := [][]Vector{}
	cnt_t := 0
  for scanner.Scan() {
	  yline := []Vector{}
    for _, x := range scanner.Text() {
		  vec := Vector{}
			vec.block = string([]rune{x})
			vec.checked = false
      yline = append(yline, vec)
    }
		yx = append(yx, yline)
		cnt_t += 1
		if cnt_t == n { break }
  }
	for y := 0; y < n; y++ {
	  for x := 0; x < m; x++ {
		  if y == 0 && x == 0 {
			  vec := Vector{[]string{"r", "b"}, true, -1, "."}
				yx[y][x] = vec
			}
		}
	}
	fmt.Println("initial", yx)
  for true {
	  for y := 0; y < n; y++ {
	    for x := 0; x < m; x++ {
			  if yx[y][x].checked == false {
				   x_from_vec := Vector{}
				   for _x := x; _x >= 0; _x-- {
						  if yx[y][x].block == "#" { continue }  
							// #が出現したら探索終わり
						  if yx[y][_x].block == "#" { break }
							x_from_vec = yx[y][_x]
						  if x_from_vec.checked {
							  fmt.Println(x_from_vec, y, x)
							}
					 }
				   y_from_vec := Vector{}
				   for _y := y; _y >= 0; _y-- {
						  if yx[y][x].block == "#" { continue }  
							// #が出現したら探索終わり
						  if yx[_y][x].block == "#" { break }
							y_from_vec = yx[_y][x]
						  if y_from_vec.checked {
							  fmt.Println("y_decline", y_from_vec, y, x)
							}
					 }
					 // 右にいくとき
					 if "r" == x_from_vec.vector[0] {
					   fmt.Println("ans r cost 0")
					 }
					 fmt.Println(y_from_vec)
					 if len(y_from_vec.vector) == 2 && "b" == y_from_vec.vector[1] {
					   fmt.Println("ans b cost 0")
					 }
				}
		  }
	  }
		break
	}
 }
