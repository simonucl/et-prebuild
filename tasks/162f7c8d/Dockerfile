FROM ubuntu:22.04

# Help text from %help / %runscript
# Container for ETL exercise. Open a shell with:
#   apptainer exec <container>.sif /bin/bash
# The starter ETL workspace is at /home/user/etl/

ENV LC_ALL=C
ENV LANG=C

RUN set -e && \
    echo "Updating APT and installing prerequisites..." && \
    apt-get update -qq && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3-pip \
        jq \
        ca-certificates \
        && apt-get clean && rm -rf /var/lib/apt/lists/*

RUN echo "Installing pytest and jsonschema..." && \
    pip3 install --no-cache-dir pytest jsonschema

RUN echo "Creating initial ETL workspace..." && \
    install -d -m 0755 /home/user/etl/raw && \
    install -d -m 0755 /home/user/etl/schema

RUN cat > /home/user/etl/raw/events.json <<'EOF'
[
  {
    "id": "123e4567-e89b-12d3-a456-426614174000",
    "timestamp": "2023-06-01T12:00:00Z",
    "type": "click",
    "payload": {
      "element_id": "btn_signup"
    }
  },
  {
    "id": "123e4567-e89b-12d3-a456-426614174001",
    "timestamp": "2023-06-01T12:05:00Z",
    "type": "view",
    "payload": {
      "page": "/home"
    }
  },
  {
    "id": "not-a-uuid",
    "timestamp": "2023-06-01T12:10:00Z",
    "type": "purchase",
    "payload": {
      "amount": 19.99
    }
  },
  {
    "id": "123e4567-e89b-12d3-a456-426614174002",
    "timestamp": "invalid-date",
    "type": "click",
    "payload": {
      "element_id": "btn_login"
    }
  },
  {
    "id": "123e4567-e89b-12d3-a456-426614174003",
    "timestamp": "2023-06-01T12:15:00Z",
    "type": "purchase",
    "payload": {
      "amount": 49.99
    }
  }
]
EOF

RUN chmod 0644 /home/user/etl/raw/events.json

RUN cat > /home/user/etl/schema/event_schema.json <<'EOF'
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "Event",
  "type": "object",
  "required": ["id", "timestamp", "type", "payload"],
  "properties": {
    "id": {
      "type": "string",
      "pattern": "^[a-f0-9-]{36}$"
    },
    "timestamp": {
      "type": "string",
      "format": "date-time"
    },
    "type": {
      "type": "string",
      "enum": ["click", "view", "purchase"]
    },
    "payload": {
      "type": "object"
    }
  },
  "additionalProperties": true
}
EOF

RUN chmod 0644 /home/user/etl/schema/event_schema.json && \
    chmod 755 /home/user

# End of Dockerfile