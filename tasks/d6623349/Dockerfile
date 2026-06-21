FROM ubuntu:22.04

# Update package index and install required tools
RUN apt-get update -y && \
    apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        jq \
        ca-certificates

# Install pytest and jsonschema via pip (latest versions)
RUN pip3 install --no-cache-dir pytest jsonschema

# Create initial directory structure
RUN mkdir -p /home/user/monitoring

# Create alert-schema.json
RUN cat > /home/user/monitoring/alert-schema.json << 'EOF'
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "required": ["id", "service", "severity", "timestamp"],
  "properties": {
    "id":        { "type": "string" },
    "service":   { "type": "string" },
    "severity":  { "type": "string",
                   "enum": ["low", "medium", "high", "critical"] },
    "timestamp": { "type": "string",
                   "format": "date-time" }
  },
  "additionalProperties": false
}
EOF

# Create alerts.json
RUN cat > /home/user/monitoring/alerts.json << 'EOF'
[
  {
    "id": "a1",
    "service": "auth",
    "severity": "high",
    "timestamp": "2023-09-12T10:33:00Z"
  },
  {
    "id": "a2",
    "service": "billing",
    "severity": "critical",
    "timestamp": "2023-09-12T10:35:27Z"
  },
  {
    "id": 100,
    "service": "db",
    "severity": "urgent",
    "timestamp": "not a date"
  }
]
EOF

# Ensure correct permissions (readable, non-executable)
RUN chmod -R a+r /home/user/monitoring

# Set permissions on home directory
RUN chmod 755 /home/user

# Remove apt caches to reduce image size
RUN apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Labels
LABEL Author="Monitoring-Platform Task Preparer"
LABEL Description="Environment with initial JSON files, pytest, jsonschema, and jq for the monitoring-platform assignment."

WORKDIR /home/user