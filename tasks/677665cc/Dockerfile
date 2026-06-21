# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# Author label from Apptainer %labels
LABEL Author="Auto-generated for Localhost Vulnerability Scan task"

# Refresh package index and install required packages
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked set -eux && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y \
        python3 \
        python3-pip \
        nmap \
        net-tools \
        iproute2 \
        --no-install-recommends && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install pytest for the grader
RUN --mount=type=cache,target=/root/.cache/pip pip3 install --no-cache-dir pytest

# Create a non-privileged user with home directory /home/user
RUN set -eux && \
    if ! id -u user >/dev/null 2>&1; then \
        useradd -m -s /bin/bash user; \
    fi && \
    chown -R user:user /home/user

# Ensure the user’s local bin directory is on PATH for interactive shells
RUN echo 'export PATH=$HOME/.local/bin:$PATH' > /etc/profile.d/10-user-local-bin.sh

# Permissions from %environment
RUN chmod 755 /home/user

# Propagate local user-installed Python tools
ENV PATH=/home/user/.local/bin:$PATH

# ------------------------------------------------------------------
# Help text from Apptainer %help
#
# This container provides a clean Ubuntu 22.04 environment with:
#   • python3 and pip
#   • pytest (for the autograder)
#   • nmap and common networking tools
#
# The scan-results file /home/user/scan_results/localhost_scan.txt
# intentionally does NOT exist at build time.
# ------------------------------------------------------------------