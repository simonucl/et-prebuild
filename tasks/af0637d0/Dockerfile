FROM ubuntu:22.04

# Update package list and install Python and pytest
RUN apt-get update -y && \
    apt-get install -y python3 python3-pip && \
    pip3 install --no-cache-dir pytest

# ------------------------------------------------------------------
# Create the initial filesystem state expected by the grading tests
# ------------------------------------------------------------------
RUN mkdir -p /home/user/configs

# 1. /home/user/configs/ssh_config.yaml  (exactly 3 lines)
RUN cat > /home/user/configs/ssh_config.yaml <<'EOF'
# OpenSSH configuration
PermitRootLogin: yes
MaxSessions: 10
EOF

# 2. /home/user/configs/service_limits.toml  (exactly 3 lines)
RUN cat > /home/user/configs/service_limits.toml <<'EOF'
# System service limits
max_open_files = 1024
max_user_processes = 512
EOF

# Ensure the non-root runtime user can read/write the files
RUN chmod -R a+rwX /home/user && \
    chmod 755 /home/user

# Labels
LABEL Author="Task Preparer"
LABEL Description="Base container for the hardening exercise with initial config files and pytest installed."