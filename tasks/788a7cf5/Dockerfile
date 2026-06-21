# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# ------------------------------------------------------------------
# Install system packages
# ------------------------------------------------------------------
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        python3-jsonschema \
        jq \
        ca-certificates && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Install Python testing framework
RUN --mount=type=cache,target=/root/.cache/pip pip3 install --no-cache-dir pytest

# ------------------------------------------------------------------
# Prepare initial exercise data
# ------------------------------------------------------------------
RUN mkdir -p /home/user/incident_responder

# incidents.json
RUN cat > /home/user/incident_responder/incidents.json <<'JSONDATA'
[
  {"id": 1001, "timestamp": "2024-05-21T13:33:12Z", "severity": "low",    "message": "Disk usage at 70%"},
  {"id": 1002, "timestamp": "2024-05-21T13:35:44Z", "severity": "high",   "message": "Unauthorized login attempt detected"},
  {"id": 1003, "timestamp": "2024-05-21T13:36:00Z", "severity": "medium", "message": "CPU load exceeds threshold"},
  {"id": 1004, "timestamp": "2024-05-21T13:37:10Z", "severity": "high",   "message": "Suspicious outbound traffic detected"}
]
JSONDATA

# incident_schema.json
RUN cat > /home/user/incident_responder/incident_schema.json <<'SCHEMADATA'
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "array",
  "items": {
    "type": "object",
    "required": ["id", "timestamp", "severity", "message"],
    "properties": {
      "id":        { "type": "integer" },
      "timestamp": { "type": "string",  "format": "date-time" },
      "severity":  { "type": "string",  "enum": ["low", "medium", "high"] },
      "message":   { "type": "string" }
    }
  }
}
SCHEMADATA

# Set permissions (world-readable, dir executable)
RUN chmod 644 /home/user/incident_responder/incidents.json \
              /home/user/incident_responder/incident_schema.json && \
    chmod 755 /home/user/incident_responder

# ------------------------------------------------------------------
# Runtime message (from %runscript)
# ------------------------------------------------------------------
CMD echo "Incident responder exercise container." && \
    echo "Initial data is located in /home/user/incident_responder."