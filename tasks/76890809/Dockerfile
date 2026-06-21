# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# %post
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked set -eux && \
    DEBIAN_FRONTEND=noninteractive apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y \
        python3 \
        python3-venv \
        python3-pip \
        ca-certificates && \
    rm -rf /var/lib/apt/lists/*

# Install pytest for the grading infrastructure
RUN --mount=type=cache,target=/root/.cache/pip pip3 install --no-cache-dir pytest

# Create a regular user `user` with home directory /home/user, if not present
RUN if ! id -u user >/dev/null 2>&1; then \
        useradd -m -u 1000 -s /bin/bash user; \
    fi

# Ensure the home directory is owned by the correct user
RUN chown -R user:user /home/user

# %environment
RUN chmod 755 /home/user
ENV LANG=C.UTF-8
ENV LC_ALL=C.UTF-8

# %runscript
# Apptainer container for the incident diagnostics task. Use as needed.