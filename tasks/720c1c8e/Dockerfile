# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# Install Python 3, pip and pytest
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest && \
    rm -rf /var/lib/apt/lists/*

# Create non-privileged user “user” with home directory /home/user
RUN set -e && \
    if ! id -u user >/dev/null 2>&1; then \
        useradd -m -s /bin/bash user; \
    fi && \
    chown -R user:user /home/user

# Guarantee the migration artefacts do NOT exist at build time
RUN rm -rf /home/user/migration

# Environment setup
RUN chmod 755 /home/user
ENV PATH="/usr/local/bin:/usr/bin:/bin"

# Default entrypoint just executes the given command
ENTRYPOINT ["bash", "-c", "exec \"$@\"", "--"]