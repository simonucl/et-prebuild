# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# Help / metadata from %labels
# Author: qa-bot
# Description: Container with initial JSON fixtures and schema for QA automation assignment.

ENV PATH="$PATH:$HOME/.local/bin"

RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked set -e && \
    echo "Updating package lists and installing base tools..." && \
    apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        jq \
        ca-certificates && \
    rm -rf /var/lib/apt/lists/*

RUN --mount=type=cache,target=/root/.cache/pip echo "Installing Python packages..." && \
    pip3 install --no-cache-dir pytest jsonschema

RUN echo "Creating initial directory structure and fixture files..." && \
    mkdir -p /home/user/qa/json_samples

RUN cat > /home/user/qa/user_schema.json <<'EOF'
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "User",
  "type": "object",
  "required": ["id", "name", "email", "roles"],
  "properties": {
    "id":    { "type": "integer", "minimum": 1 },
    "name":  { "type": "string",  "minLength": 1 },
    "email": { "type": "string",  "format": "email" },
    "roles": { "type": "array",   "items": { "type": "string" } }
  }
}
EOF

RUN cat > /home/user/qa/json_samples/user1.json <<'EOF'
{"id":1,"name":"Alice","email":"alice@example.com","roles":["admin","qa"]}
EOF

RUN cat > /home/user/qa/json_samples/user2.json <<'EOF'
{"id":0,"name":"Bob","email":"not-an-email","roles":[]}
EOF

RUN cat > /home/user/qa/json_samples/user3.json <<'EOF'
{"id":2,"name":"Charlie","email":"charlie@example.com","roles":["dev"]}
EOF

RUN echo "Setting permissions..." && chmod -R ugo+rwX /home/user/qa && chmod 755 /home/user