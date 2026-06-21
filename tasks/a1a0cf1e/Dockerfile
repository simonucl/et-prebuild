# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# help
# Container for uptime-check validation task.
# Use jq and a JSON-Schema validator as described in the assignment.

ENV PATH=/usr/local/bin:/usr/local/sbin:/usr/bin:/usr/sbin:/bin:/sbin

RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked set -e && \
    export DEBIAN_FRONTEND=noninteractive && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
        jq \
        python3 \
        python3-pip && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN --mount=type=cache,target=/root/.cache/pip pip3 install --no-cache-dir \
        pytest \
        jsonschema \
        check-jsonschema

RUN mkdir -p /home/user/data && \
    mkdir -p /home/user/output && \
    chmod 0777 /home/user/output

RUN cat <<'EOF' > /home/user/data/uptime_checks.json
[{"service_name":"auth","status":"OK","response_time_ms":120},{"service_name":"billing","status":"FAIL","response_time_ms":310},{"service_name":"search","status":"OK","response_time_ms":95},{"service_name":"cart","status":"OK","response_time_ms":210},{"service_name":"email","status":"FAIL","response_time_ms":275}]
EOF

RUN cat <<'EOF' > /home/user/data/uptime_schema.json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "array",
  "items": {
    "type": "object",
    "required": ["service_name", "status", "response_time_ms"],
    "properties": {
      "service_name": { "type": "string" },
      "status": { "type": "string", "enum": ["OK", "FAIL"] },
      "response_time_ms": { "type": "number", "minimum": 0 }
    },
    "additionalProperties": false
  }
}
EOF

RUN chmod 0644 /home/user/data/uptime_checks.json /home/user/data/uptime_schema.json && \
    chmod 755 /home/user

CMD echo "Container for uptime-check validation task." && \
    echo "Use jq and a JSON-Schema validator as described in the assignment."