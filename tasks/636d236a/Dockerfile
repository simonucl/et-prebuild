# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# Basic development tools and Python
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest && \
    groupadd -g 1000 user && \
    useradd -m -u 1000 -g 1000 -s /bin/bash user && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Set permissions on the home directory
RUN chmod 755 /home/user

# Environment variables
ENV PATH="/usr/local/bin:$PATH"

# Set working directory and user
WORKDIR /home/user
USER user

# Default action: start an interactive shell
CMD ["/bin/bash"]