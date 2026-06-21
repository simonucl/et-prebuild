# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# Help:
# This Apptainer image sets up the pristine filesystem state required for the
# "Junior Compliance Analyst" exercise. It installs Python 3, pytest, and
# provides the initial configuration and reference data under
# /home/user/compliance/ for students to work with.

LABEL Author="junior-compliance-setup"
LABEL Description="Initial container for the Junior Compliance Analyst task"

# Environment variables
ENV PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin

RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 python3-pip && \
    pip3 install --no-cache-dir pytest && \
    mkdir -p /home/user/compliance/configs && \
    mkdir -p /home/user/compliance/reference

RUN cat <<'EOF' > /home/user/compliance/configs/sshd_config
# Example SSHD Configuration
Port 22
PermitRootLogin yes
PasswordAuthentication yes
ChallengeResponseAuthentication yes
EOF

RUN cat <<'EOF' > /home/user/compliance/reference/ports_sample.log
tcp        0      0 0.0.0.0:22            0.0.0.0:*               LISTEN
tcp        0      0 127.0.0.1:631         0.0.0.0:*               LISTEN
udp        0      0 0.0.0.0:68            0.0.0.0:*              
EOF

RUN cat <<'EOF' > /home/user/compliance/reference/services_sample.log
sshd
cupsd
dhclient
systemd
EOF

RUN chmod -R a+rX /home/user/compliance && \
    chmod 755 /home/user