FROM ubuntu:24.04

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    bash \
    ca-certificates \
    coreutils \
    findutils \
    golang-go \
    python3 \
    unzip \
    zip \
  && rm -rf /var/lib/apt/lists/*

RUN mkdir -p /app/module-src /app/goproxy/example.internal/edge/ratelimit/@v

RUN cat > /app/module-src/go.mod <<'EOF'
module example.internal/edge/ratelimit

go 1.22
EOF

RUN cat > /app/module-src/limiter.go <<'EOF'
package ratelimit

import "time"

// Window describes an allow-list rate limit window.
type Window struct {
	Name     string
	Limit    int
	Interval time.Duration
}

func Allows(w Window, events int) bool {
	if w.Limit <= 0 {
		return false
	}
	return events <= w.Limit
}
EOF

RUN cat > /app/module-src/limiter_test.go <<'EOF'
package ratelimit

import (
	"testing"
	"time"
)

func TestAllows(t *testing.T) {
	w := Window{Name: "edge", Limit: 3, Interval: time.Minute}
	if !Allows(w, 3) {
		t.Fatal("limit should allow boundary count")
	}
	if Allows(w, 4) {
		t.Fatal("limit should reject overage")
	}
}
EOF

RUN cat > /app/module-src/README.md <<'EOF'
# edge ratelimit

Small internal module used by the edge gateway integration tests.
EOF

RUN cat > /app/goproxy/example.internal/edge/ratelimit/@v/list <<'EOF'
v0.8.0
EOF

RUN cat > /app/goproxy/example.internal/edge/ratelimit/@v/v0.9.0.info <<'EOF'
{"Version":"v0.9.0","Time":"2026-06-01 10:30:00"}
EOF

RUN cat > /app/goproxy/example.internal/edge/ratelimit/@v/v0.9.0.mod <<'EOF'
module example.internal/edge/ratelimit

go 1.21
EOF

RUN cd /app/module-src && zip -q -r /app/goproxy/example.internal/edge/ratelimit/@v/example.internal_edge_ratelimit_v0.9.0.zip .

RUN cat > /app/goproxy/example.internal/edge/ratelimit/@v/proxy-manifest.json <<'EOF'
{"module":"example.internal/edge/ratelimit","version":"v0.9.0","files":[],"zip_sha256":"broken","mod_sha256":"broken","info_sha256":"broken"}
EOF

RUN chmod -R a+rX /app/module-src /app/goproxy
