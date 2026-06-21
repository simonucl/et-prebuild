FROM ubuntu:22.04

# Help: Container pre-populated with service configuration files for the
# "deployment summary" exercise.  Python3 and pytest are installed so that
# the grading framework can run its tests.

RUN set -e && \
    echo "Updating APT and installing Python & pip..." && \
    apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends python3 python3-pip && \
    echo "Installing pytest..." && \
    pip3 install --no-cache-dir pytest && \
    echo "Creating initial directory structure and configuration files..." && \
    mkdir -p /home/user/release/configs && \
    chmod 777 /home/user/release

# frontend.ini
RUN cat > /home/user/release/configs/frontend.ini << 'EOF'
[production]
version = 5.4.2
port = 8080

[staging]
version = 5.4.2-rc1
port = 8081
EOF

# backend.ini
RUN cat > /home/user/release/configs/backend.ini << 'EOF'
[production]
version = 2.18.0
port = 9090

[staging]
version = 2.18.0-rc1
port = 9091
EOF

# worker.ini
RUN cat > /home/user/release/configs/worker.ini << 'EOF'
[production]
version = 1.3.7
port = 7070

[staging]
version = 1.3.7-rc2
port = 7071
EOF

RUN chmod 644 /home/user/release/configs/*.ini && \
    chmod 755 /home/user

LABEL Author="Automated build for deployment-summary task"