FROM ubuntu:22.04

LABEL Author="credential-rotation-task"
LABEL Description="Environment prepared for credential rotation exercise"

RUN set -e && apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
    python3 \
    python3-pip \
    jq \
    ca-certificates

RUN pip3 install --no-cache-dir pytest

RUN mkdir -p /home/user/cred_rotation

RUN cat >/home/user/cred_rotation/old_creds.json <<'EOF'
{
  "service": "payments-api",
  "environment": "production",
  "credentials": {
    "access_key": "AKIAOLD1234567",
    "secret_key": "oldsecret",
    "created_at": "2023-01-15T08:30:00Z",
    "version": 1
  }
}
EOF

RUN cat >/home/user/cred_rotation/creds_schema.json <<'EOF'
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "required": ["service", "environment", "credentials"],
  "properties": {
    "service": { "type": "string" },
    "environment": { "type": "string" },
    "credentials": {
      "type": "object",
      "required": ["access_key", "secret_key", "created_at", "version"],
      "properties": {
        "access_key": { "type": "string", "pattern": "^AKIA[0-9A-Z]{8,}$" },
        "secret_key": { "type": "string" },
        "created_at": { "type": "string", "format": "date-time" },
        "version": { "type": "integer", "minimum": 1 }
      }
    }
  }
}
EOF

RUN chmod 755 /home/user && chmod 755 /home/user/cred_rotation && chmod 644 /home/user/cred_rotation/*.json

ENV PATH="$PATH:$HOME/.local/bin"

CMD echo "Container for credential-rotation task. Execute your rotation commands here."