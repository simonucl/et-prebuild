FROM ubuntu:22.04

# Help section (from Apptainer %help if any existed)
# No %help content provided.

RUN set -e && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        jq \
        ca-certificates && \
    pip3 install --no-cache-dir pytest

RUN mkdir -p /home/user/iot/deployment && \
    mkdir -p /home/user/iot/logs

RUN cat > /home/user/iot/deployment/device_status.json <<'EOF'
[
  {
    "device_id": "edge-therm-01",
    "status": "online",
    "ip": "192.168.10.21"
  },
  {
    "device_id": "edge-therm-02",
    "status": "offline",
    "ip": "192.168.10.22"
  },
  {
    "device_id": "edge-therm-03",
    "status": "online",
    "ip": "192.168.10.23"
  },
  {
    "device_id": "edge-therm-04",
    "status": "maintenance",
    "ip": "192.168.10.24"
  },
  {
    "device_id": "edge-therm-05",
    "status": "offline",
    "ip": "192.168.10.25"
  }
]
EOF

RUN cat > /home/user/iot/deployment/device_status_schema.json <<'EOF'
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "Device Status Schema",
  "type": "object",
  "properties": {
    "device_id": { "type": "string" },
    "status":     { "type": "string" },
    "ip":         { "type": "string", "format": "ipv4" }
  },
  "required": ["device_id", "status", "ip"],
  "additionalProperties": false
}
EOF

RUN chmod -R 777 /home/user/iot

RUN apt-get clean && rm -rf /var/lib/apt/lists/*

ENV LANG=C.UTF-8
ENV LC_ALL=C.UTF-8

RUN chmod 755 /home/user