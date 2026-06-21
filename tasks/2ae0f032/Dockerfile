FROM ubuntu:22.04

# Install Python and pytest
RUN set -eux && \
    export DEBIAN_FRONTEND=noninteractive && \
    apt-get update && \
    apt-get install -y --no-install-recommends python3 python3-pip && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Create project directory
RUN mkdir -p /home/user/projects/helloapp

# Create template unit file
RUN cat > /home/user/projects/helloapp/helloapp.service.template <<'EOF'
[Unit]
Description=Hello App Service

[Service]
Type=simple
ExecStart=@SCRIPT_PATH@
EnvironmentFile=@ENV_PATH@

[Install]
WantedBy=default.target
EOF

# Create executable script
RUN cat > /home/user/projects/helloapp/helloapp.sh <<'EOF'
#!/usr/bin/env bash
echo "Hello, world!"
EOF

RUN chmod +x /home/user/projects/helloapp/helloapp.sh

# Ensure /home/user exists and is writable
RUN chmod -R a+rwx /home/user

# Labels
LABEL Author="oncall-config-assistant"

# Help text
# Container providing the initial state for the “helloapp” configuration-management task.
# Includes:
#   - Project directory at /home/user/projects/helloapp/
#   - Template systemd unit with placeholders
#   - Executable helloapp.sh script
# Pytest is installed for validation.