FROM ubuntu:22.04

# Install Python and pytest
RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y python3 python3-pip && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Create a regular user with UID 1000 if it doesn't already exist
RUN if ! id -u 1000 >/dev/null 2>&1; then \
        groupadd -g 1000 user || true; \
        useradd -m -u 1000 -g 1000 -s /bin/bash user || true; \
    fi

# Ensure /home/user exists and is writable by any unprivileged user
RUN mkdir -p /home/user && \
    chmod 0777 /home/user

# Set up the audit_sample directory with the required structure
RUN AUDIT_DIR="/home/user/audit_sample" && \
    mkdir -p "${AUDIT_DIR}" && \
    chmod 0755 "${AUDIT_DIR}" && \
    # Regular files
    install -m 0644 /dev/null "${AUDIT_DIR}/file1.conf" && \
    install -m 0755 /dev/null "${AUDIT_DIR}/script.sh" && \
    install -m 0600 /dev/null "${AUDIT_DIR}/secret.key" && \
    # Sub-directory
    mkdir -p "${AUDIT_DIR}/config" && \
    chmod 0700 "${AUDIT_DIR}/config"

# Set permissions on home directory
RUN chmod 755 /home/user

# Labels
LABEL Author="security-auditor-task"
LABEL Description="Environment for security auditing task with pytest installed"