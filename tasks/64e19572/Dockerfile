# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# ------------------------------------------------------------------
# Author: Automatic container setup for INI audit task
# ------------------------------------------------------------------

RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest && \
    rm -rf /var/lib/apt/lists/*

# ------------------------------------------------------------------
# Create required initial filesystem state for the task
# ------------------------------------------------------------------

# Home and config directories
RUN mkdir -p /home/user/configs && \
    chmod 0777 /home/user && \
    chmod 0777 /home/user/configs

# INI file: /home/user/configs/app1.ini
RUN cat >/home/user/configs/app1.ini <<'EOF'
[General]
Version=2.0
ComplianceLevel=PCI-DSS
Encryption=AES256

[Network]
Port=443
Protocol=HTTPS
EOF

# INI file: /home/user/configs/app2.ini
RUN cat >/home/user/configs/app2.ini <<'EOF'
[General]
Version=1.4
ComplianceLevel=HIPAA
Encryption=AES128

[Network]
Port=8443
Protocol=HTTPS
EOF

# Make sure the files are readable and writable by any user who runs
RUN chmod 0666 /home/user/configs/app1.ini /home/user/configs/app2.ini

# ------------------------------------------------------------------
# Environment setup (from %environment)
# ------------------------------------------------------------------
RUN chmod 755 /home/user

LABEL Author="Automatic container setup for INI audit task"