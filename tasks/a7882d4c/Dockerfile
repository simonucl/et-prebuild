FROM ubuntu:22.04

# Install Python tooling and pytest
RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3-pip \
        python3-setuptools \
        python3-wheel && \
    pip3 install --no-cache-dir pytest

# Create an unprivileged user `user`
RUN adduser --disabled-password --gecos "" user

# Set up the initial fixture
RUN mkdir -p /home/user/incoming && \
    touch /home/user/incoming/app-1.0.0-linux-amd64.tar.gz && \
    touch /home/user/incoming/plugin-2.3.4.zip && \
    touch /home/user/incoming/agent.v1.5.1.bin

# Ensure correct permissions
RUN chown -R user:user /home/user && \
    chmod 0755 /home/user && \
    chmod 0755 /home/user/incoming && \
    chmod 0644 /home/user/incoming/*

# Environment variables
ENV PATH="/home/user/.local/bin:$PATH"

# Default entrypoint
ENTRYPOINT ["/bin/sh", "-c", "exec \"$@\"", "--"]