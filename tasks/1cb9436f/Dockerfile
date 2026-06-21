FROM ubuntu:22.04

# Help text
# Container for the diagnostics validation exercise.
# This container only provides the initial dataset and tooling.

ENV PATH="/usr/local/bin:/usr/bin:/bin:$PATH"

RUN set -eux && \
    export DEBIAN_FRONTEND=noninteractive && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        jq \
        ca-certificates && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* && \
    pip3 install --no-cache-dir pytest jsonschema && \
    mkdir -p /home/user/diagnostics/raw && \
    mkdir -p /home/user/diagnostics/schema

RUN cat <<'EOF' > /home/user/diagnostics/raw/log1.json
{
  "service": "auth",
  "status": "running",
  "errors": []
}
EOF

RUN cat <<'EOF' > /home/user/diagnostics/raw/log2.json
{
  "service": "payments",
  "status": "degraded",
  "errors": ["timeout connecting to db", "retry failure"]
}
EOF

RUN cat <<'EOF' > /home/user/diagnostics/raw/log3.json
{
  "status": "running",
  "errors": []
}
EOF

RUN cat <<'EOF' > /home/user/diagnostics/schema/diagnostic.schema.json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "required": ["service", "status", "errors"],
  "properties": {
    "service": { "type": "string" },
    "status":  { "type": "string" },
    "errors":  {
      "type": "array",
      "items": { "type": "string" }
    }
  },
  "additionalProperties": false
}
EOF

RUN chmod -R a+rwX /home/user/diagnostics && \
    find /home/user/diagnostics -type f -exec chmod 644 {} \; && \
    chmod 755 /home/user

CMD echo "Container for the diagnostics validation exercise." && echo "This container only provides the initial dataset and tooling."