# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# Refresh package lists and install Python + pip, then install pytest
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip set -eux && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest && \
    mkdir -p /home/user && \
    chmod 0777 /home/user && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Set environment variables
ENV PATH="/usr/local/bin:/usr/bin:/bin:${PATH}"

# Ensure correct permissions on home directory
RUN chmod 755 /home/user

# Default command: start a login shell
CMD ["bash", "-l"]