FROM ubuntu:22.04

# %post
RUN set -e && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
        jq \
        python3 \
        python3-pip && \
    rm -rf /var/lib/apt/lists/*

RUN pip3 install --no-cache-dir pytest

RUN mkdir -p /home/user/accounts

RUN cat <<'JSON' > /home/user/accounts/users.json
[
  {
    "username": "alice",
    "email": "alice@example.com",
    "active": true,
    "roles": ["admin", "editor"]
  },
  {
    "username": "bob",
    "email": "bob@example.com",
    "active": false,
    "roles": ["viewer"]
  },
  {
    "username": "carol",
    "email": "carol@example.com",
    "active": true,
    "roles": ["editor"]
  },
  {
    "username": "dave",
    "email": "dave@example.com",
    "active": true,
    "roles": ["viewer", "support"]
  },
  {
    "username": "eve",
    "email": "eve@example.com",
    "active": false,
    "roles": ["suspended"]
  }
]
JSON

RUN cat <<'JSON' > /home/user/accounts/users_schema.json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "UserList",
  "type": "array",
  "items": {
    "type": "object",
    "required": ["username", "email", "active", "roles"],
    "properties": {
      "username": { "type": "string", "pattern": "^[a-z]+$" },
      "email": { "type": "string", "format": "email" },
      "active": { "type": "boolean" },
      "roles": {
        "type": "array",
        "items": { "type": "string" },
        "minItems": 1
      }
    },
    "additionalProperties": false
  }
}
JSON

RUN chmod 0755 /home/user && \
    chmod 0755 /home/user/accounts && \
    chmod 0644 /home/user/accounts/users.json && \
    chmod 0644 /home/user/accounts/users_schema.json

# %environment
ENV PATH="/usr/local/bin:/usr/bin:/bin:$PATH"

# %labels
LABEL Author="user-accounts-prep"
LABEL Description="Environment for the 'user-accounts' exercise with initial data and tooling."