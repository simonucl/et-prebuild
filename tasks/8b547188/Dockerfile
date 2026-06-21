# Author="Container setup for Filter High-Priority Open Tickets task"
# Description="Provides jq, pytest, and initial data files under /home/user/data"

FROM ubuntu:22.04

RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        jq \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN mkdir -p /home/user/data

RUN cat <<'EOF' > /home/user/data/support_tickets.json
[
  {
    "id": "1001",
    "subject": "Cannot connect to VPN",
    "status": "open",
    "priority": "high",
    "assignee": "unassigned"
  },
  {
    "id": "1002",
    "subject": "Forgot Windows password",
    "status": "resolved",
    "priority": "medium",
    "assignee": "it_support"
  },
  {
    "id": "1003",
    "subject": "Email not syncing",
    "status": "open",
    "priority": "high",
    "assignee": "unassigned"
  }
]
EOF

RUN cat <<'EOF' > /home/user/data/ticket_schema.json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "array",
  "items": {
    "type": "object",
    "required": ["id", "subject", "status", "priority", "assignee"],
    "properties": {
      "id":        { "type": "string" },
      "subject":   { "type": "string" },
      "status":    { "type": "string", "enum": ["open", "in_progress", "resolved", "closed"] },
      "priority":  { "type": "string", "enum": ["low", "medium", "high"] },
      "assignee":  { "type": "string" }
    },
    "additionalProperties": false
  }
}
EOF

RUN chmod -R a+r /home/user/data && chmod 777 /home/user && chmod 755 /home/user

ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8
ENV PATH="$PATH:$(python3 -m site --user-base)/bin"