FROM ubuntu:22.04

# Help:
# This Apptainer image provides the initial filesystem state for ticket #5678.
# Pytest is pre-installed and the required directories/files are in place so the
# student can resolve the ticket without elevated privileges.

RUN set -e && \
    echo "Updating APT and installing Python tooling..." && \
    apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y \
        python3 \
        python3-pip \
        python3-setuptools --no-install-recommends && \
    rm -rf /var/lib/apt/lists/*

RUN echo "Installing pytest via pip..." && \
    pip3 install --no-cache-dir pytest

RUN echo "Creating initial directory structure..." && \
    mkdir -p /home/user/tickets/ticket_5678 && \
    mkdir -p /home/user/ticket_logs

RUN echo "Populating /home/user/tickets/ticket_5678/app.conf with baseline content..." && \
    cat <<'EOF' > /home/user/tickets/ticket_5678/app.conf
[General]
name = sample-app
version = 1.4.2

[Network]
host = 127.0.0.1
port = 8080

[Logging]
level = info
EOF

RUN echo "Setting permissive permissions so the unprivileged runtime user can write..." && \
    chmod -R 0777 /home/user/tickets /home/user/ticket_logs && \
    chmod 0666 /home/user/tickets/ticket_5678/app.conf

RUN chmod 755 /home/user

LABEL Author="Configuration Ticket 5678 Image"