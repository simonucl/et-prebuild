# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# ------------------------------------------------------------------
# Author label (from %labels section)
# ------------------------------------------------------------------
LABEL Author="Performance-metric initial state creator"

# ------------------------------------------------------------------
# Install dependencies
# ------------------------------------------------------------------
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3-pip \
        jq \
        ca-certificates && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN --mount=type=cache,target=/root/.cache/pip pip3 install --no-cache-dir pytest jsonschema

# ------------------------------------------------------------------
# Create directory structure
# ------------------------------------------------------------------
RUN mkdir -p /home/user/app/metrics/raw

# ------------------------------------------------------------------
# schema.json
# ------------------------------------------------------------------
RUN cat > /home/user/app/metrics/schema.json <<'JSON'
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "Performance Metrics",
  "type": "object",
  "required": ["timestamp", "cpu", "mem", "req_per_sec"],
  "properties": {
    "timestamp": { "type": "integer" },
    "cpu": { "type": "number", "minimum": 0, "maximum": 100 },
    "mem": { "type": "number", "minimum": 0, "maximum": 100 },
    "req_per_sec": { "type": "integer", "minimum": 0 }
  },
  "additionalProperties": false
}
JSON

# ------------------------------------------------------------------
# metric1.json
# ------------------------------------------------------------------
RUN cat > /home/user/app/metrics/raw/metric1.json <<'JSON'
{ "timestamp": 1680000000, "cpu": 45.5, "mem": 62.3, "req_per_sec": 850 }
JSON

# ------------------------------------------------------------------
# metric2.json
# ------------------------------------------------------------------
RUN cat > /home/user/app/metrics/raw/metric2.json <<'JSON'
{ "timestamp": 1680000600, "cpu": 52.0, "mem": 70.1, "req_per_sec": 920 }
JSON

# ------------------------------------------------------------------
# metric3_bad.json
# ------------------------------------------------------------------
RUN cat > /home/user/app/metrics/raw/metric3_bad.json <<'JSON'
{ "timestamp": "1680001200", "cpu": 47.2, "mem": 65.0 }
JSON

# ------------------------------------------------------------------
# Permissions: owner-writeable (0644) so no root privileges needed
# ------------------------------------------------------------------
RUN chmod 644 /home/user/app/metrics/schema.json /home/user/app/metrics/raw/*.json && \
    chmod 755 /home/user

# ------------------------------------------------------------------
# Help (from %help section - none provided)
# ------------------------------------------------------------------