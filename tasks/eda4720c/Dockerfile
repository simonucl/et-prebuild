FROM ubuntu:22.04

# Labels
LABEL Author="Container setup for site-admin exercise"

# Environment
ENV PATH=/usr/local/bin:/usr/bin:/bin:$PATH

# Core packages and Python testing framework
RUN set -e && \
    apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y \
        python3 \
        python3-pip \
        jq \
        ca-certificates && \
    pip3 install --no-cache-dir pytest

# Prepare the initial exercise data
RUN mkdir -p /home/user/site_admin_data && \
    chmod 755 /home/user/site_admin_data

# Create users.json
RUN cat <<'EOF' > /home/user/site_admin_data/users.json
[
  { "id": 1, "username": "alice", "active": true,  "roles": ["admin", "editor"] },
  { "id": 2, "username": "bob",   "roles": ["editor"] },
  { "id": 3, "active": false,     "roles": ["viewer"] },
  { "id": 4, "username": "carol", "active": "yes",  "roles": ["editor"] },
  { "id": 5, "username": "dan",   "active": false, "roles": ["viewer", "commenter"] }
]
EOF

# Create user_schema.json
RUN cat <<'EOF' > /home/user/site_admin_data/user_schema.json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "required": ["id", "username", "active", "roles"],
  "properties": {
    "id":       { "type": "integer" },
    "username": { "type": "string"  },
    "active":   { "type": "boolean" },
    "roles": {
      "type": "array",
      "items": { "type": "string" }
    }
  },
  "additionalProperties": false
}
EOF

RUN chmod 644 /home/user/site_admin_data/users.json /home/user/site_admin_data/user_schema.json

WORKDIR /home/user

CMD ["/bin/bash"]