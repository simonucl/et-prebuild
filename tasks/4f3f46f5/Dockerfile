FROM ubuntu:22.04

# Labels from %labels
LABEL Author="Auto-generated definition for help-desk tickets task"
LABEL Description="Container with baseline files and tools for validating and filtering help-desk tickets"

RUN set -e && \
    echo "Updating APT and installing required packages..." && \
    apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        python3-jsonschema \
        jq \
        ca-certificates && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN echo "Installing pytest via pip..." && \
    python3 -m pip install --no-cache-dir --upgrade pip && \
    python3 -m pip install --no-cache-dir pytest

RUN echo "Creating /home/user with starter JSON files..." && \
    mkdir -p /home/user && \
    chmod 0777 /home/user

RUN cat > /home/user/tickets.json << 'EOF'
[
  {
    "id": 1001,
    "title": "Router reboot required",
    "status": "open",
    "team": "network"
  },
  {
    "id": 1002,
    "title": "Email account locked",
    "status": "closed",
    "team": "support"
  },
  {
    "id": 1003,
    "title": "Switch firmware upgrade",
    "status": "open",
    "team": "network"
  },
  {
    "id": 1004,
    "title": "Printer not responding",
    "status": "open",
    "team": "support"
  }
]
EOF

RUN chmod 0644 /home/user/tickets.json

RUN cat > /home/user/ticket_schema.json << 'EOF'
{
  "type": "array",
  "items": {
    "type": "object",
    "required": [ "id", "title", "status", "team" ],
    "properties": {
      "id":    { "type": "integer" },
      "title": { "type": "string"  },
      "status":{ "type": "string"  },
      "team":  { "type": "string"  }
    }
  }
}
EOF

RUN chmod 0644 /home/user/ticket_schema.json && \
    chmod 755 /home/user

ENV LANG=C.UTF-8
ENV LC_ALL=C.UTF-8
ENV PYTHONUNBUFFERED=1