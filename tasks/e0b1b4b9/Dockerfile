FROM ubuntu:22.04

# Labels
LABEL Author="AI Assistant"
LABEL Description="Docker image for mobile build-agent health task with pytest pre-installed."

# Update package lists and install Python tooling
RUN apt-get update && \
    apt-get install -y --no-install-recommends python3 python3-pip && \
    pip3 install --no-cache-dir pytest

# Prepare the required initial filesystem state under /home/user
RUN mkdir -p /home/user/build_logs

# Create the agent_status.log file with the exact expected contents
RUN cat > /home/user/build_logs/agent_status.log <<'EOF'
agent_id:A01 status:OK latency_ms:94
agent_id:A12 status:FAIL latency_ms:256
agent_id:B03 status:OK latency_ms:101
agent_id:C07 status:FAIL latency_ms:305
agent_id:D99 status:OK latency_ms:87
EOF

# Ensure correct permissions
RUN chmod 755 /home/user/build_logs && \
    chmod 644 /home/user/build_logs/agent_status.log

# Guarantee that the reports directory does NOT exist yet
RUN rm -rf /home/user/build_reports || true

# Clean up apt caches to keep image lean
RUN apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /home/user