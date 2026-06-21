# syntax=docker/dockerfile:1
FROM ubuntu:22.04

LABEL Author="TaskGenerator" \
      Description="Container for QA task: prepare pristine INI file and install pytest"

# Update apt repositories and install Python tooling
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip set -e && \
    apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest

# Create initial directory structure and INI file
RUN set -e && \
    mkdir -p /home/user/webapp/config && \
    cat > /home/user/webapp/config/settings.ini << 'EOF'
[server]
host = 0.0.0.0
port = 8080

[email]
smtp_host = mail.example.com
smtp_port = 587
username = notify@example.com
password = mailingR0cks!

[database]
host = 172.16.24.10
port = 5432
user = webapp
password = s3cr3t!

[feature_flags]
dark_mode = true
beta_payments = false
EOF

# Ensure readable files and executable search paths for non-root users and clean up
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked set -e && \
    chmod 755 /home/user && \
    chmod -R 755 /home/user/webapp && \
    chmod 644 /home/user/webapp/config/settings.ini && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# This container provides the pristine environment required for the QA automation task.
# It contains:
#   • Python 3 and pytest
#   • /home/user/webapp/config/settings.ini with the exact required contents
#
# Students should run their solution scripts separately.