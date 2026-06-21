FROM ubuntu:22.04

RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y \
        python3 \
        python3-pip \
        jq \
        curl \
        ca-certificates && \
    pip3 install --no-cache-dir pytest && \
    mkdir -p /home/user/cloud_costs/raw && \
    mkdir -p /home/user/cloud_costs/schema

RUN cat > /home/user/cloud_costs/raw/weekly_costs.json <<'EOF'
[
  {
    "account_id": "acc-001",
    "service": "EC2",
    "cost": 800,
    "currency": "USD",
    "week": "2023-W25"
  },
  {
    "account_id": "acc-002",
    "service": "S3",
    "cost": 1200,
    "currency": "USD",
    "week": "2023-W25"
  },
  {
    "account_id": "acc-003",
    "service": "RDS",
    "cost": 1500,
    "currency": "USD",
    "week": "2023-W25"
  },
  {
    "account_id": "acc-004",
    "service": "Lambda",
    "cost": 400,
    "currency": "USD",
    "week": "2023-W25"
  }
]
EOF

RUN cat > /home/user/cloud_costs/schema/cloud_cost_report.schema.json <<'EOF'
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "array",
  "items": {
    "type": "object",
    "additionalProperties": false,
    "required": ["account_id", "service", "cost", "currency", "week"],
    "properties": {
      "account_id": { "type": "string" },
      "service":     { "type": "string" },
      "cost":        { "type": "number" },
      "currency":    { "type": "string" },
      "week":        { "type": "string" }
    }
  }
}
EOF

RUN chmod -R a+rX /home/user

ENV PATH=/usr/local/bin:/usr/local/sbin:/usr/bin:/usr/sbin:/bin:/sbin:$PATH

WORKDIR /home/user