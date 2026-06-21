# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# Labels from Apptainer definition
LABEL Author="SOC-Task-Builder"
LABEL Description="Base image for SSH failed-login analysis assignment"

# ----------------------------
# 1. Install dependencies
# ----------------------------
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# ---------------------------------------------
# 2. Prepare pre-existing directory & logs
# ---------------------------------------------
RUN set -e && \
    mkdir -p /home/user && \
    chmod 0777 /home/user && \
    mkdir -p /home/user/syslogs

RUN cat > /home/user/syslogs/auth.log.2023-07-21 <<'EOF'
Jul 21 10:03:12 server sshd[12345]: Failed password for invalid user admin from 192.168.1.10 port 54321 ssh2
Jul 21 10:05:44 server sshd[12346]: Accepted password for user1 from 192.168.1.3 port 54322 ssh2
Jul 21 11:15:01 server sshd[12347]: Failed password for root from 10.0.0.5 port 60001 ssh2
Jul 21 11:16:10 server sshd[12348]: Failed password for invalid user test from 192.168.1.10 port 60002 ssh2
Jul 21 12:00:00 server cron[12349]: (root) CMD (some job)
Jul 21 12:10:55 server sshd[12350]: Failed password for root from 192.168.1.10 port 60003 ssh2
Jul 21 13:15:23 server sshd[12351]: Failed password for invalid user admin from 10.0.0.5 port 60004 ssh2
EOF

RUN cat > /home/user/syslogs/auth.log.2023-07-22 <<'EOF'
Jul 22 09:00:22 server sshd[22345]: Failed password for root from 10.0.0.5 port 60101 ssh2
Jul 22 09:02:13 server sshd[22346]: Failed password for invalid user admin from 10.0.0.5 port 60102 ssh2
Jul 22 09:05:44 server sshd[22347]: Accepted password for user2 from 192.168.1.3 port 60103 ssh2
Jul 22 10:15:01 server sshd[22348]: Failed password for root from 8.8.8.8 port 60104 ssh2
Jul 22 10:25:30 server sshd[22349]: Failed password for invalid user guest from 10.0.0.5 port 60105 ssh2
Jul 22 11:45:10 server sshd[22350]: Failed password for root from 192.168.1.10 port 60106 ssh2
Jul 22 12:30:22 server sshd[22351]: Failed password for root from 192.168.1.10 port 60107 ssh2
EOF

RUN chmod -R a+r /home/user/syslogs

# ----------------------------
# Environment configuration
# ----------------------------
ENV PATH="/usr/local/bin:/usr/bin:/bin"

RUN set -e && \
    chmod 755 /home/user && \
    if [ ! -e /usr/bin/python ] && [ -e /usr/bin/python3 ]; then \
        ln -s /usr/bin/python3 /usr/bin/python; \
    fi

# ----------------------------
# Help (from Apptainer %help)
# ----------------------------
# This image sets up the initial state required for the
# "SSH failed-login analysis" programming task.
# It pre-installs Python and pytest, and populates the directory
# /home/user/syslogs with two authentication log files.
# Learners will run inside the container (without root privileges)
# and create their own artefacts under /home/user/analysis.