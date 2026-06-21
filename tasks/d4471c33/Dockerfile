FROM ubuntu:22.04

# Labels
LABEL Author="on-call configuration-manager exercise"

# Install minimal tooling plus pytest
RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3-pip \
        procps \
        iproute2 \
        net-tools && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Create user and set up home directory
RUN useradd -m -s /bin/bash user && \
    mkdir -p /home/user/config_audit && \
    chmod 755 /home/user && \
    chmod 700 /home/user/config_audit && \
    chown -R user:user /home/user

# Set environment variables
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

# Set working directory
WORKDIR /home/user

USER user

# Help information (as comment):
# This container sets up the initial state for the configuration-audit task.
# It pre-installs pytest and ensures the directory /home/user/config_audit
# exists (owned by the invoking user) every time the container starts,
# while leaving the snapshot log file absent for the student to create.