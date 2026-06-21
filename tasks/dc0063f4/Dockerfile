FROM ubuntu:22.04

# Labels
LABEL Author="benchmark-task-setup"
LABEL Description="Container image that prepares the initial state for the CLI micro-benchmark task (v1 vs v2)."

# Environment
ENV PATH=/usr/local/bin:/usr/bin:/bin:$PATH

# Install packages and pytest
RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        time && \
    pip3 install --no-cache-dir pytest && \
    rm -rf /var/lib/apt/lists/*

# Prepare directory structure
RUN mkdir -p /home/user/app/v1 && \
    mkdir -p /home/user/app/v2

# v1 script
RUN cat >/home/user/app/v1/process_data.sh <<'EOF'
#!/usr/bin/env bash
echo "Processing data – v1"
sleep 1
EOF

RUN chmod 755 /home/user/app/v1/process_data.sh

# v2 script
RUN cat >/home/user/app/v2/process_data.sh <<'EOF'
#!/usr/bin/env bash
echo "Processing data – v2"
sleep 0.25
EOF

RUN chmod 755 /home/user/app/v2/process_data.sh

# Ensure /home/user has safe default permissions
RUN chmod 755 /home/user

WORKDIR /home/user