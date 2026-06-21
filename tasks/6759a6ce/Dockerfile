# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# Install Python tooling and pytest, and set up /home/user
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip set -eux && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
        python3-pip \
        python3-setuptools \
        python3-wheel && \
    pip3 install --no-cache-dir pytest && \
    mkdir -p /home/user && \
    chmod 0755 /home/user && \
    rm -rf /var/lib/apt/lists/*

# Ensure correct permissions and PATH for user-installed Python binaries
ENV PATH="/home/user/.local/bin:${PATH}"

# Default command (equivalent to Apptainer runscript exec "$@")
CMD ["bash"]