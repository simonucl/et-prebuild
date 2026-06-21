FROM ubuntu:22.04

# Labels
LABEL Author="incident-preparer"
LABEL Description="Initial data image for 'Validate Incident JSON Records' exercise"

# Help documentation (as comments)
# This container image provides the initial dataset and required tooling
# (Python 3, jsonschema, pytest, jq) for the "Validate Incident JSON Records,
# Filter Critical Events, and Produce Summaries" exercise.

# Update apt package index and install runtime dependencies
RUN set -e && \
    echo "Updating apt package index and installing runtime dependencies ..." && \
    apt-get update -qq && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        jq \
        ca-certificates && \
    rm -rf /var/lib/apt/lists/*

# Install pytest and JSON-Schema runtime
RUN echo "Installing pytest and JSON-Schema runtime ..." && \
    pip3 install --no-cache-dir pytest jsonschema

# Create incident data directories
RUN echo "Creating incident data directories ..." && \
    mkdir -p /home/user/incidents/2023-09-15

# Create schema file
RUN cat > /home/user/incidents/2023-09-15/incident_schema.json <<'EOF'
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "required": [ "event_id", "severity", "event_type", "timestamp", "source_ip" ],
  "properties": {
    "event_id":   { "type": "string" },
    "severity":   { "type": "string", "enum": ["low","medium","high","critical"] },
    "event_type": { "type": "string" },
    "timestamp":  { "type": "string", "format": "date-time" },
    "source_ip":  { "type": "string", "format": "ipv4" },
    "details":    { "type": "object" }
  },
  "additionalProperties": true
}
EOF

# Create event1.json
RUN cat > /home/user/incidents/2023-09-15/event1.json <<'EOF'
{
  "event_id": "evt-1001",
  "severity": "high",
  "event_type": "unauthorized_access",
  "timestamp": "2023-09-15T14:22:01Z",
  "source_ip": "192.168.10.5",
  "details": {
    "user": "alice",
    "location": "us-east-1"
  }
}
EOF

# Create event2.json
RUN cat > /home/user/incidents/2023-09-15/event2.json <<'EOF'
{
  "event_id": "evt-1002",
  "severity": "medium",
  "event_type": "file_modification",
  "timestamp": "2023-09-15T15:05:33Z",
  "source_ip": "10.0.0.8",
  "details": {
    "file": "/etc/passwd",
    "user": "bob"
  }
}
EOF

# Create event3.json (intentionally malformed – missing source_ip)
RUN cat > /home/user/incidents/2023-09-15/event3.json <<'EOF'
{
  "event_id": "evt-1003",
  "severity": "critical",
  "event_type": "denial_of_service",
  "timestamp": "2023-09-15T16:47:12Z",
  "details": {
    "packets": 1000000
  }
}
EOF

# Set permissions
RUN echo "Setting permissions (directories 0755, files 0644, writable for all users under /home/user/incidents) ..." && \
    chmod -R a+rX /home/user/incidents && \
    find /home/user/incidents -type f -exec chmod a+rw {} \; && \
    find /home/user/incidents -type d -exec chmod a+rwX {} \; && \
    chmod 755 /home/user

# Environment variables
ENV PATH="$PATH:/root/.local/bin"