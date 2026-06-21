# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# Labels from Apptainer definition
LABEL Author="Incident-Response Exercise Environment"
LABEL Description="Container pre-configured for the SSH failed-login burst task"

# Install Python tooling and pytest
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        ca-certificates && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Prepare filesystem layout
RUN set -e && \
    mkdir -p /home/user/logs && \
    mkdir -p /home/user/output

# Create the ground-truth authentication log with exact contents
RUN cat > /home/user/logs/incident.log <<'EOF'
Feb  7 10:15:32 server sshd[2234]: Failed password for invalid user admin from 192.168.1.10 port 53422 ssh2
Feb  7 10:15:35 server sshd[2235]: Failed password for invalid user root from 203.0.113.55 port 53423 ssh2
Feb  7 10:15:38 server sshd[2236]: Failed password for invalid user admin from 192.168.1.10 port 53424 ssh2
Feb  7 10:15:40 server sshd[2237]: Failed password for invalid user guest from 198.51.100.23 port 53425 ssh2
Feb  7 10:15:42 server sshd[2238]: Failed password for invalid user admin from 192.0.2.44 port 53426 ssh2
Feb  7 10:15:45 server sshd[2239]: Failed password for invalid user root from 203.0.113.55 port 53427 ssh2
Feb  7 10:15:48 server sshd[2240]: Failed password for invalid user admin from 192.168.1.10 port 53428 ssh2
Feb  7 10:15:50 server sshd[2241]: Failed password for invalid user admin from 198.51.100.23 port 53429 ssh2
EOF

# Ensure the directories and files are readable by non-root users
RUN chmod 755 /home/user && \
    chmod -R 755 /home/user/logs /home/user/output && \
    chmod 644 /home/user/logs/incident.log