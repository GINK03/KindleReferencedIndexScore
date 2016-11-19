package main

/*
* Golangでmath/bigで最大公約数を計算する際にコピペで用いることができます。
* big.Intは、newで匿名のインスタンスを作成することで、使用する関数にアクセスすることがベストプラクティスになりうる可能性があります
 */
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
	op_sum, op_mul := big.NewInt(0), big.NewInt(0)
	op_sum.Add(&a, &b)
	op_mul.Mul(&a, &b)
	fmt.Println(new(big.Int).GCD(nil, nil, op_sum, op_mul))
}
