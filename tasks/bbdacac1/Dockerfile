# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# Basic tooling and Python test framework
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked set -eux && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3-pip \
        jq \
        ca-certificates && \
    rm -rf /var/lib/apt/lists/*

RUN --mount=type=cache,target=/root/.cache/pip pip3 install --no-cache-dir pytest

# Prepare working directory and seed data
RUN mkdir -p /home/user/audit && \
    chmod 777 /home/user /home/user/audit || true

# permissions.json
RUN cat > /home/user/audit/permissions.json <<'EOF'
{
  "users": [
    { "username": "alice", "uid": 1001, "permissions": ["read", "write"] },
    { "username": "bob", "uid": 1002, "permissions": ["read"] },
    { "username": "carol", "uid": 0, "permissions": ["read", "write", "execute", "admin"] },
    { "username": "dave", "uid": 1003, "permissions": ["read", "write", "execute"] }
  ]
}
EOF

# permissions.schema.json
RUN cat > /home/user/audit/permissions.schema.json <<'EOF'
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "required": ["users"],
  "properties": {
    "users": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["username", "uid", "permissions"],
        "properties": {
          "username": { "type": "string" },
          "uid": { "type": "integer" },
          "permissions": {
            "type": "array",
            "items": { "type": "string" }
          }
        }
      }
    }
  }
}
EOF

# Set read-only permissions for the seed files
RUN chmod 644 /home/user/audit/permissions.json /home/user/audit/permissions.schema.json

# Environment setup
RUN chmod 755 /home/user
ENV LC_ALL=C.UTF-8