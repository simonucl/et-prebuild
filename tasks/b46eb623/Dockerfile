# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# Labels
LABEL Author="incident_lab_setup"
LABEL Description="Base image for awk/sed incident-response exercise"

# Install tools and pytest
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip set -eux && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        gawk \
        sed \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest

# Create directory tree
RUN mkdir -p /home/user/incident_logs

# Write auth.log file
RUN cat > /home/user/incident_logs/auth.log <<'LOGEOF'
# Authentication log file sample
# Generated on 2023-09-25

Sep 25 12:15:01 server1 sshd[12345]: Failed password for invalid user admin from 203.0.113.45 port 54321 ssh2
Sep 25 12:15:05 server1 sshd[12346]: Failed password for invalid user root from 198.51.100.23 port 54322 ssh2
Sep 25 12:15:10 server1 sshd[12347]: Failed password for invalid user admin from 203.0.113.45 port 54323 ssh2
Sep 25 12:15:15 server1 sshd[12348]: Failed password for invalid user test from 192.0.2.77 port 54324 ssh2
Sep 25 12:15:20 server1 sshd[12349]: Failed password for invalid user admin from 203.0.113.45 port 54325 ssh2
Sep 25 12:15:26 server1 sshd[12350]: Accepted password for validuser from 10.0.0.1 port 54326 ssh2
Sep 25 12:15:30 server1 sshd[12351]: Failed password for invalid user guest from 198.51.100.23 port 54327 ssh2
LOGEOF

# Permissions
RUN chmod -R 777 /home/user && chmod 755 /home/user

# Clean up
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked apt-get clean && rm -rf /var/lib/apt/lists/*

# Environment
ENV LC_ALL=C
ENV PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin

# Default command
CMD ["/bin/bash"]