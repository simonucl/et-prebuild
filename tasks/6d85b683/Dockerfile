# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# Update package lists and install Python tooling required for the task
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-venv \
        python3-pip && \
    pip3 install --no-cache-dir pytest && \
    mkdir -p /home/user && \
    chmod 0777 /home/user && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Ensure correct permissions on the home directory
RUN chmod 755 /home/user

# Make sure the pytest entry-point installed by pip is on the PATH
ENV PATH="/usr/local/bin:${PATH}"

# Default command: start an interactive shell
CMD ["/bin/bash"]