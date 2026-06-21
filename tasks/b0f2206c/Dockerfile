# syntax=docker/dockerfile:1
# Derived from localimage ./ubuntu_22.04.sif
FROM ubuntu:22.04

# Install Python, pip, pytest, and required packages
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        ca-certificates \
        bash && \
    pip3 install --no-cache-dir pytest && \
    mkdir -p /home/user && \
    chmod 755 /home/user && \
    mkdir -p /home/user/deployments && \
    chmod 755 /home/user/deployments && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Provide minimal .bashrc
RUN printf "# Minimal bashrc for test harness – do not modify\n" > /home/user/.bashrc && \
    chmod 644 /home/user/.bashrc

# Environment settings
ENV PATH=/usr/local/bin:/usr/bin:/bin:$PATH

# Labels
LABEL Author="release-manager task setup" \
      Description="Base image prepared for DevOps environment-variable task" \
      Version="1.0"