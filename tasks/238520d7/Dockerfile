FROM ubuntu:22.04

# Basic tooling
RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        jq \
        python3 \
        python3-pip \
        ca-certificates && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Python testing framework
RUN pip3 install --no-cache-dir pytest

# Prepare workspace and configuration snapshots
RUN mkdir -p /home/user/configs && \
    chmod 777 /home/user && \
    chmod 777 /home/user/configs

# previous_config.json
RUN cat <<'EOF' > /home/user/configs/previous_config.json
{
  "service": {
    "name": "demo",
    "enabled": true,
    "port": 8080
  },
  "logging": {
    "level": "info",
    "file": "/var/log/demo.log"
  },
  "version": "1.0.0"
}
EOF

# new_config.json
RUN cat <<'EOF' > /home/user/configs/new_config.json
{
  "service": {
    "name": "demo",
    "enabled": false,
    "port": 9090
  },
  "logging": {
    "level": "debug",
    "file": "/var/log/demo-debug.log"
  },
  "version": "1.1.0"
}
EOF

# schema.json
RUN cat <<'EOF' > /home/user/configs/schema.json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "required": ["service", "logging", "version"],
  "properties": {
    "service": {
      "type": "object",
      "required": ["name", "enabled", "port"],
      "properties": {
        "name":    { "type": "string"  },
        "enabled": { "type": "boolean" },
        "port":    { "type": "integer", "minimum": 1, "maximum": 65535 }
      }
    },
    "logging": {
      "type": "object",
      "required": ["level", "file"],
      "properties": {
        "level": { "type": "string", "enum": ["debug", "info", "warn", "error"] },
        "file":  { "type": "string" }
      }
    },
    "version": { "type": "string" }
  }
}
EOF

# Reasonable default permissions for JSON files
RUN chmod 644 /home/user/configs/*.json

ENV PATH=/usr/local/bin:$PATH
ENV HOME=/home/user

RUN chmod 755 /home/user