FROM ubuntu:22.04

# Labels
LABEL Author="edge-computing-task-builder"
LABEL Description="Environment prepared for IoT gateway reachability task – contains initial inventory and pytest"

# Basic OS packages
RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        iputils-ping \
        parallel \
        ca-certificates && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Python packages (pytest for task validation)
RUN pip3 install --no-cache-dir --upgrade pip && \
    pip3 install --no-cache-dir pytest

# Prepare initial filesystem state
# Ensure /home/user exists with open permissions
RUN mkdir -p /home/user && \
    chmod 755 /home/user

# Create the required inventory file with exact content
RUN cat > /home/user/iot_targets.csv <<'EOF'
device01,127.0.0.1
device02,10.255.255.1
EOF

# Make sure the file ends with a newline and is world-readable
RUN echo >> /home/user/iot_targets.csv && \
    chmod 644 /home/user/iot_targets.csv

# Do NOT create /home/user/logs – must be absent

WORKDIR /home/user