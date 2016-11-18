package main

import (
	"bufio"
)

var rdr = bufio.NewReaderSize(os.Stdin, 10000000)

func gets() string {
	buf := make([]byte, 0, 10000000)
	for {
		l, p, _ := rdr.ReadLine()
		buf = append(buf, l...)
		if !p {
			break
		}
	}
	return string(buf)
}
