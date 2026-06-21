# Using Ubuntu 22.04 as base (Bootstrap: localimage not supported in Docker)
FROM ubuntu:22.04

# Update and install required packages
RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        jq \
        ca-certificates && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install pytest
RUN pip3 install --no-cache-dir pytest

# Prepare initial filesystem state
RUN mkdir -p /home/user/deployment

# Create schema.json
RUN cat <<'EOF' > /home/user/deployment/schema.json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "Update descriptor",
  "type": "object",
  "required": ["update_id", "version", "status"],
  "properties": {
    "update_id": { "type": "string" },
    "version": {
      "type": "string",
      "pattern": "^(0|[1-9][0-9]*)\\.(0|[1-9][0-9]*)\\.(0|[1-9][0-9]*)$"
    },
    "status": {
      "type": "string",
      "enum": ["pending", "applied"]
    }
  },
  "additionalProperties": false
}
EOF

# Create updates.json
RUN cat <<'EOF' > /home/user/deployment/updates.json
[
  {"update_id":"udp-100","version":"1.2.0","status":"pending"},
  {"update_id":"udp-101","version":"1.2","status":"pending"},
  {"update_id":"udp-102","version":"1.3.0","status":"deploying"},
  {"update_id":"udp-103","version":"1.4.0","status":"applied"},
  {"update_id":"udp-104","version":"1.5.0"}
]
EOF

# Permissions setup
RUN chmod 777 /home/user/deployment && \
    chmod 644 /home/user/deployment/schema.json /home/user/deployment/updates.json && \
    chmod 755 /home/user

# Environment variables
ENV LANG=C.UTF-8
ENV LC_ALL=C.UTF-8