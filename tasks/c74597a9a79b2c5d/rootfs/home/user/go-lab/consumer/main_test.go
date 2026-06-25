package main

import (
	"reflect"
	"testing"

	"example.com/acme/metricfilter/filter"
)

func TestCanonicalLabels(t *testing.T) {
	got := filter.CanonicalLabels(map[string]string{" Region ": " us-east-1 ", "Job": " api ", "empty": " "})
	want := []string{"job=api", "region=us-east-1"}
	if !reflect.DeepEqual(got, want) {
		t.Fatalf("CanonicalLabels() = %#v, want %#v", got, want)
	}
}
