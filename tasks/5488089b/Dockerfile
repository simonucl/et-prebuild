FROM ubuntu:22.04

# Install required packages
RUN set -e && \
    apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        python3-setuptools \
        ca-certificates \
        locales \
        grep \
        gawk \
        coreutils \
        nano \
        less && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install pytest
RUN pip3 install --no-cache-dir pytest

# Create CI directory structure and logs
RUN mkdir -p /home/user/ci/logs

RUN cat << 'EOF' > /home/user/ci/logs/service-auth.log
[2023-07-15T10:05:23Z] INFO Starting auth service
[2023-07-15T10:05:24Z] ERROR Failed to connect to DB
[2023-07-15T10:05:25Z] INFO Retrying connection
[2023-07-15T10:05:26Z] ERROR Failed to connect to DB
[2023-07-15T10:05:27Z] INFO Service shutting down
EOF

RUN cat << 'EOF' > /home/user/ci/logs/service-payment.log
2023-07-15 10:06:11 INFO  Payment processor started
2023-07-15 10:06:12 ERROR Gateway timeout
2023-07-15 10:06:13 ERROR Gateway timeout
2023-07-15 10:06:14 INFO  Payment retried OK
EOF

# Permissions
RUN chmod -R 777 /home/user

# Environment variables from %environment
RUN chmod 755 /home/user
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

LABEL Author="task-setup-automation"
LABEL Description="Apptainer image pre-populated with CI log files and pytest installed."