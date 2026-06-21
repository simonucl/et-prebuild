FROM ubuntu:22.04

# Author: hardening-task
# Version: v1.0
# Purpose: Initial state for JSON hardening exercise

RUN set -e && \
    apt-get update && \
    apt-get install -y --no-install-recommends python3 python3-pip jq && \
    rm -rf /var/lib/apt/lists/*

RUN pip3 install --no-cache-dir pytest jsonschema

RUN useradd -m -s /bin/bash user

RUN install -d -m 0755 /home/user/hardening

RUN cat >/home/user/hardening/config.json <<'EOF'
{
  "system": "webserver",
  "ssh": {
    "permitRootLogin": "no",
    "passwordAuthentication": "no"
  },
  "firewall": {
    "portsOpen": [22, 80, 443]
  }
}
EOF

RUN cat >/home/user/hardening/schema.json <<'EOF'
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "required": ["system", "ssh", "firewall"],
  "properties": {
    "system": { "type": "string" },
    "ssh": {
      "type": "object",
      "required": ["permitRootLogin", "passwordAuthentication"],
      "properties": {
        "permitRootLogin": {
          "type": "string",
          "enum": ["yes", "no"]
        },
        "passwordAuthentication": {
          "type": "string",
          "enum": ["yes", "no"]
        }
      },
      "additionalProperties": false
    },
    "firewall": {
      "type": "object",
      "required": ["portsOpen"],
      "properties": {
        "portsOpen": {
          "type": "array",
          "items": { "type": "integer" }
        }
      },
      "additionalProperties": false
    }
  },
  "additionalProperties": false
}
EOF

RUN chown -R user:user /home/user && chmod 755 /home/user

ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8