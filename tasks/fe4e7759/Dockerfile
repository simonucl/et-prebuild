FROM ubuntu:22.04

# Help / labels
LABEL Author="task-prep-script"
LABEL Description="Environment for CSV-to-JSON data wrangling task with pytest pre-installed."

# ------------------------------------------------------------------
# Basic packages + pytest
# ------------------------------------------------------------------
RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get -y install --no-install-recommends \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# ------------------------------------------------------------------
# Create required directories and seed input data
# ------------------------------------------------------------------
RUN mkdir -p /home/user/device_data && \
    mkdir -p /home/user/output

RUN cat > /home/user/device_data/devices.csv <<'EOF'
id,location,temp_c,battery_v
dev-001,roof-nw,68.3,3.7
dev-002,roof-se,72.4,3.8
dev-003,lab-south,75.0,3.6
dev-004,lab-north,70.0,3.9
dev-005,warehouse,71.2,3.8
EOF

# ------------------------------------------------------------------
# Permissions
# ------------------------------------------------------------------
RUN chmod -R 0777 /home/user

# Environment variables (converted from %environment)
ENV PATH=/usr/local/bin:/usr/bin:/bin:$PATH