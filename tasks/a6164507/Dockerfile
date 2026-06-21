FROM ubuntu:22.04

# Update package lists and install required tools
RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        jq \
        python3-pip \
        ca-certificates && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install pytest
RUN pip3 install --no-cache-dir pytest

# Prepare filesystem
RUN mkdir -p /home/user/deployment && \
    chmod 0777 /home/user/deployment

# Create JSON configuration file
RUN cat > /home/user/deployment/edge_device_config.json <<'EOF'
[
  {"id":"dev-001","location":"NYC","status":"active"},
  {"id":"dev-002","location":"Berlin","status":"inactive"},
  {"id":"dev-003","location":"London","status":"active"},
  {"location":"Tokyo","status":"inactive"},
  {"id":"dev-005","location":"Paris","status":"inactive"}
]
EOF

RUN chmod 0644 /home/user/deployment/edge_device_config.json

RUN chmod 755 /home/user

# Help text
# This image provides the initial environment for the edge-computing JSON validation exercise.
# It contains:
#   - jq
#   - pytest
#   - The pre-populated /home/user/deployment/edge_device_config.json file
# Students will generate validation_report.txt inside the same directory.

LABEL Author="Container prepared for IoT rollout validation task"