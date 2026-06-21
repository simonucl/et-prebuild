# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# Install Python, pip, pytest, and procps
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip apt-get update && \
    apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        procps && \
    pip3 install --no-cache-dir pytest && \
    mkdir -p /home/user && \
    chmod 0777 /home/user && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Environment setup
ENV PATH="/usr/local/bin:/usr/bin:/bin:$PATH"

# Ensure correct permissions on home directory
RUN chmod 755 /home/user

# Default run behavior: execute whatever command is passed
ENTRYPOINT ["sh", "-c", "exec \"$@\"", "--"]