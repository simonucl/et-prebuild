package filter

import (
	"sort"
	"strings"
)

func CanonicalLabels(labels map[string]string) []string {
	out := make([]string, 0, len(labels))
	for key, value := range labels {
		key = strings.ToLower(strings.TrimSpace(key))
		value = strings.TrimSpace(value)
		if key == "" || value == "" {
			continue
		}
		out = append(out, key+"="+value)
	}
	sort.Strings(out)
	return out
}
