FROM ubuntu:22.04

# Base tooling
RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 python3-pip python3-setuptools \
        python3-pytest \
        jq \
        ca-certificates && \
    pip3 install --no-cache-dir --upgrade pip pytest

# Create initial filesystem state for the exercise
RUN mkdir -p /home/user/data && \
    mkdir -p /home/user/schemas

# ping_results.json
RUN cat > /home/user/data/ping_results.json <<'JSONDATA'
[
  {"host":"db-1","timestamp":"2023-08-01T10:00:00Z","status":"up","latency_ms":45},
  {"host":"db-1","timestamp":"2023-08-01T10:05:00Z","status":"up","latency_ms":50},
  {"host":"db-1","timestamp":"2023-08-01T10:10:00Z","status":"up","latency_ms":47},
  {"host":"db-1","timestamp":"2023-08-01T10:15:00Z","status":"up","latency_ms":46},
  {"host":"web-1","timestamp":"2023-08-01T10:00:00Z","status":"up","latency_ms":23},
  {"host":"web-1","timestamp":"2023-08-01T10:05:00Z","status":"down","latency_ms":null},
  {"host":"web-1","timestamp":"2023-08-01T10:10:00Z","status":"up","latency_ms":25},
  {"host":"web-1","timestamp":"2023-08-01T10:15:00Z","status":"up","latency_ms":22}
]
JSONDATA

# ping_result.schema.json
RUN cat > /home/user/schemas/ping_result.schema.json <<'JSONSCHEMA'
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "array",
  "items": {
    "type": "object",
    "required": ["host", "timestamp", "status", "latency_ms"],
    "properties": {
      "host":        { "type": "string" },
      "timestamp":   { "type": "string" },
      "status":      { "type": "string", "enum": ["up", "down"] },
      "latency_ms":  { "type": ["number", "null"] }
    },
    "additionalProperties": false
  }
}
JSONSCHEMA

# Permissions
RUN chmod 777 /home/user && \
    chmod 755 /home/user/data /home/user/schemas && \
    chmod 644 /home/user/data/ping_results.json && \
    chmod 644 /home/user/schemas/ping_result.schema.json

ENV PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin

WORKDIR /home/user