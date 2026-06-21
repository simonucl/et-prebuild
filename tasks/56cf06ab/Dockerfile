FROM ubuntu:22.04

# Install runtime dependencies
RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        jq \
        nodejs \
        npm \
        python3-pip \
        ca-certificates \
        curl && \
    npm install -g ajv-cli && \
    pip3 install --no-cache-dir pytest jsonschema

# Create directory skeleton expected by the tests
RUN mkdir -p /home/user/storage_audit/schema && \
    mkdir -p /home/user/storage_audit/raw_reports

# Seed the JSON-Schema file
RUN cat >/home/user/storage_audit/schema/disk_report.schema.json <<'EOF'
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "required": ["host", "generatedAt", "mounts"],
  "properties": {
    "host": { "type": "string" },
    "generatedAt": { "type": "string", "format": "date-time" },
    "mounts": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["mountPoint", "totalGB", "usedGB"],
        "properties": {
          "mountPoint": { "type": "string" },
          "totalGB": { "type": "number" },
          "usedGB": { "type": "number" }
        }
      }
    }
  }
}
EOF

# Seed the first raw report JSON document
RUN cat >/home/user/storage_audit/raw_reports/daily_storage01.json <<'EOF'
{
  "host": "storage01",
  "generatedAt": "2023-01-01T00:00:00Z",
  "mounts": [
    { "mountPoint": "/",      "totalGB": 50,  "usedGB": 25 },
    { "mountPoint": "/data",  "totalGB": 200, "usedGB": 150 }
  ]
}
EOF

# Seed the second raw report JSON document
RUN cat >/home/user/storage_audit/raw_reports/daily_storage02.json <<'EOF'
{
  "host": "storage02",
  "generatedAt": "2023-01-01T00:05:00Z",
  "mounts": [
    { "mountPoint": "/",       "totalGB": 60,  "usedGB": 35 },
    { "mountPoint": "/backup", "totalGB": 500, "usedGB": 400 }
  ]
}
EOF

# Seed the third raw report JSON document
RUN cat >/home/user/storage_audit/raw_reports/daily_storage03.json <<'EOF'
{
  "host": "storage03",
  "generatedAt": "2023-01-01T00:10:00Z",
  "mounts": [
    { "mountPoint": "/",        "totalGB": 40,  "usedGB": 10 },
    { "mountPoint": "/archive", "totalGB": 1000, "usedGB": 600 }
  ]
}
EOF

# Set permissions so the non-root user can read everything
RUN chmod 755 /home/user && \
    chmod 755 /home/user/storage_audit && \
    chmod 755 /home/user/storage_audit/schema && \
    chmod 755 /home/user/storage_audit/raw_reports && \
    chmod 644 /home/user/storage_audit/schema/disk_report.schema.json && \
    chmod 644 /home/user/storage_audit/raw_reports/daily_storage01.json && \
    chmod 644 /home/user/storage_audit/raw_reports/daily_storage02.json && \
    chmod 644 /home/user/storage_audit/raw_reports/daily_storage03.json

# NOTE: Do NOT create the logs/ or summary/ directories here;
#       they must be produced by the student's solution.

# Ensure locally installed Python utilities are discoverable
ENV PATH="/home/user/.local/bin:/usr/local/bin:$PATH"

WORKDIR /home/user

CMD ["echo", "Container for the 'disk-usage reports' task. It only provides the initial dataset and required tooling (jq, ajv)."]