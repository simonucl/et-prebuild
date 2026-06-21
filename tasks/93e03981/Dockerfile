# Converted from Apptainer definition file
FROM ubuntu:22.04

# Install required packages
RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        cron && \
    pip3 install --no-cache-dir pytest

# Create unprivileged user "user" with home directory /home/user
RUN set -e && \
    if ! id -u user >/dev/null 2>&1; then \
        if id -u 1000 >/dev/null 2>&1; then \
            useradd -m -s /bin/bash user; \
        else \
            useradd -m -u 1000 -s /bin/bash user; \
        fi; \
    fi && \
    mkdir -p /home/user && \
    chown -R user:user /home/user

# Prepare cron spool directory with correct permissions
RUN mkdir -p /var/spool/cron/crontabs && \
    chmod 1730 /var/spool/cron/crontabs && \
    chown root:crontab /var/spool/cron/crontabs

# Environment setup from %environment
# (Replacing chmod with proper Docker RUN instruction)
RUN chmod 755 /home/user

# Labels from %labels
LABEL Author="user"