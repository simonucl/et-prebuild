FROM ubuntu:22.04

# Author: Auto-generated container for configuration-manager task

# This container sets up the initial filesystem and tooling for the
# configuration-manager shell task. It provides:
#   - /home/user/configs with seed JSON files and change.log
#   - jq, jsonschema CLI, Python 3, and pytest installed and ready to use

RUN set -e && \
    apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        python3-jsonschema \
        jq \
        ca-certificates && \
    pip3 install --no-cache-dir pytest && \
    mkdir -p /home/user/configs

RUN cat <<'EOF' >/home/user/configs/app_config.json
{
  "version": "1.2.3",
  "environment": "staging",
  "services": [
    {
      "name": "web",
      "image": "example/web:latest",
      "enabled": true,
      "ports": [80, 443]
    },
    {
      "name": "db",
      "image": "postgres:13",
      "enabled": false,
      "ports": [5432]
    }
  ],
  "owner": "ops@example.com"
}
EOF

RUN cat <<'EOF' >/home/user/configs/app_schema.json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "required": ["version", "services"],
  "properties": {
    "version": { "type": "string", "pattern": "^[0-9]+\\.[0-9]+\\.[0-9]+$" },
    "environment": { "type": "string" },
    "owner": { "type": "string", "format": "email" },
    "services": {
      "type": "array",
      "minItems": 1,
      "items": {
        "type": "object",
        "required": ["name", "enabled"],
        "properties": {
          "name": { "type": "string" },
          "image": { "type": "string" },
          "enabled": { "type": "boolean" },
          "ports": {
            "type": "array",
            "items": { "type": "integer", "minimum": 1, "maximum": 65535 }
          }
        }
      }
    }
  },
  "additionalProperties": true
}
EOF

RUN echo '2023-12-31T23:59:59Z initial_seed' >/home/user/configs/change.log

RUN chmod 777 /home/user && \
    chmod 777 /home/user/configs && \
    chmod 666 /home/user/configs/change.log && \
    chmod 644 /home/user/configs/app_config.json /home/user/configs/app_schema.json

ENV PATH=/usr/local/bin:/usr/bin:/bin:$PATH