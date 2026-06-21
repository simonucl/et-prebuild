FROM ubuntu:22.04

# Labels
LABEL Author="devops-task"
LABEL Purpose="Baseline image for DevOps logging configuration exercise"

# Install Python and pytest
RUN set -eux && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y python3 python3-pip && \
    pip3 install --no-cache-dir pytest

# Build the project's initial directory structure
RUN set -eux && \
    mkdir -p /home/user/devops-demo/bin \
             /home/user/devops-demo/config \
             /home/user/devops-demo/logs

# Populate bin/run.sh (placeholder executable)
RUN cat > /home/user/devops-demo/bin/run.sh <<'EOF'
#!/usr/bin/env bash
echo "Run script placeholder"
EOF

RUN chmod +x /home/user/devops-demo/bin/run.sh

# Create the ORIGINAL logging configuration file
RUN cat > /home/user/devops-demo/config/service.conf <<'EOF'
[logging]
log_level = INFO
log_file  = ./logs/app.log
EOF

# Seed the shipping application log with ground-truth lines
RUN cat > /home/user/devops-demo/logs/app.log <<'EOF'
2023-07-01 12:00:00,001 - root - INFO  - Service started
2023-07-01 12:00:05,123 - root - DEBUG - Loaded config
2023-07-01 12:00:10,999 - root - ERROR - Connection failed
2023-07-01 12:00:15,456 - root - DEBUG - Retrying connection
2023-07-01 12:00:20,321 - root - DEBUG - Connection established
2023-07-01 12:00:25,888 - root - INFO  - Service running
2023-07-01 12:00:30,777 - root - ERROR - Timeout occurred
EOF

# Make everything writable so the non-root agent can modify files
RUN chmod -R a+rwX /home/user/devops-demo && \
    chmod 755 /home/user

# Environment variables
ENV PROJECT_ROOT=/home/user/devops-demo

WORKDIR /home/user

CMD ["/bin/bash"]