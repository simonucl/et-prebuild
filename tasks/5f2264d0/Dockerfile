# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# ------------------------------------------------------------------
# Labels from Apptainer %labels
# ------------------------------------------------------------------
LABEL Author="ComplianceExercise" \
      Description="Initial state for INI compliance report exercise"

# ------------------------------------------------------------------
# Environment variables from %environment
# ------------------------------------------------------------------
ENV DEBIAN_FRONTEND=noninteractive \
    LC_ALL=C.UTF-8 \
    LANG=C.UTF-8

# ------------------------------------------------------------------
# Install Python tooling (pip) and pytest for the automated tests
# ------------------------------------------------------------------
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip set -e && \
    apt-get update && \
    apt-get install -y --no-install-recommends python3-pip && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# ------------------------------------------------------------------
# Create the required initial file structure and contents
# ------------------------------------------------------------------
RUN set -e && \
    mkdir -p /home/user && \
    chmod 1777 /home/user && \
    mkdir -p /home/user/config && \
    chmod 755 /home/user/config

RUN cat >/home/user/config/system.cfg <<'EOF'
[General]
hostname=server01
os=ubuntu
version=20.04

[Security]
firewall=enabled
selinux=disabled
password_policy=weak

[Compliance]
data_encryption=aes256
logging=disabled
EOF

RUN chmod 644 /home/user/config/system.cfg

# ------------------------------------------------------------------
# %help
# This container image sets up the initial environment needed for the
# compliance-report task. It installs pytest for the test harness and
# pre-creates /home/user/config/system.cfg with the exact contents
# specified in the exercise.
# ------------------------------------------------------------------