FROM ubuntu:22.04

# Labels
LABEL Author="benchmark-setup"

# Update package index and install required system packages.
RUN set -eux && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3-pip \
        time \
        ca-certificates && \
    rm -rf /var/lib/apt/lists/*

# Install pytest for the test harness.
RUN pip3 install --no-cache-dir pytest

# Create user home and scripts directory.
RUN mkdir -p /home/user/scripts

# Provide the existing workflow script.
RUN cat >/home/user/scripts/workflow.sh <<'EOF'
#!/usr/bin/env bash
# Simulated workflow
sleep 0.05
echo "Workflow step completed"
EOF

# Ensure correct permissions
RUN chmod 755 /home/user/scripts && \
    chmod 755 /home/user/scripts/workflow.sh && \
    chmod 777 /home/user

# Environment variables
ENV PATH="/usr/local/bin:/usr/bin:/bin:$PATH"

# Default entrypoint
ENTRYPOINT ["/bin/bash", "-c", "exec \"$@\"", "--"]