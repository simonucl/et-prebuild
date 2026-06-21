FROM ubuntu:22.04

# Help text
# This container sets up the starting environment for the “IoT connection report” exercise.
# directory layout:
#   /home/user/edge_devices/
#       ├─ devices.json (initial inventory)
#       └─ reports/ (empty, writable; student writes report here)
# The container also has pytest pre-installed for automated grading.

RUN set -e && \
    apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3-pip \
        jq \
        ca-certificates && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

RUN python3 -m pip install --no-cache-dir --upgrade pip
RUN python3 -m pip install --no-cache-dir pytest

RUN mkdir -p /home/user/edge_devices/reports

RUN cat <<'EOF' > /home/user/edge_devices/devices.json
[
  {"id":"sensor-1","ip":"10.0.0.11","status":"online"},
  {"id":"sensor-2","ip":"10.0.0.12","status":"offline"},
  {"id":"gateway-1","ip":"10.0.0.1","status":"online"},
  {"id":"camera-1","ip":"10.0.0.20","status":"offline"},
  {"id":"sensor-3","ip":"10.0.0.13","status":"online"}
]
EOF

RUN chmod 0777 /home/user/edge_devices/reports
RUN chmod 755 /home/user

LABEL Author="IoT-Edge Exercise Generator"
LABEL Description="Container for the IoT connection report task. Includes pytest and initial filesystem state."