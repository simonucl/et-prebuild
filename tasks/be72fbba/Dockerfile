FROM ubuntu:22.04

# Install required packages
RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y \
        python3 \
        python3-pip \
        diffutils \
        patch && \
    pip3 install --no-cache-dir pytest

# Prepare the initial file system state expected by the test-suite
RUN mkdir -p /home/user/audit && \
    chmod 0777 /home/user/audit

# Baseline configuration snapshot
RUN cat > /home/user/audit/server.cfg.orig <<'EOF'
# Server configuration
Port=8080
EnableSSH=false
MaxUsers=10
EOF

# Newly scanned configuration snapshot
RUN cat > /home/user/audit/server.cfg.new <<'EOF'
# Server configuration
Port=2222
EnableSSH=true
MaxUsers=20
Logging=verbose
EOF

# Readable by all; originals should not need to be modified by the agent
RUN chmod 0644 /home/user/audit/server.cfg.orig /home/user/audit/server.cfg.new && \
    chmod 755 /home/user

# Labels
LABEL Author="Security Audit Task Maintainer"
LABEL Description="Ubuntu 22.04 base image pre-loaded with audit configs and pytest."