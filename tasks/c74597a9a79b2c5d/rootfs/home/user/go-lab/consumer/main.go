package main

import (
	"fmt"

	"example.com/acme/metricfilter/filter"
)

func main() {
	fmt.Println(filter.CanonicalLabels(map[string]string{" Region ": " us-east-1 ", "Job": " api "}))
}
