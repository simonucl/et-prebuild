# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# %post section
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip set -e && \
    echo "Updating package index and installing Python tooling..." && \
    apt-get update -qq && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        python3-setuptools \
        ca-certificates \
        build-essential && \
    echo "Installing pytest for the runtime test harness..." && \
    python3 -m pip install --no-cache-dir --upgrade pip && \
    python3 -m pip install --no-cache-dir pytest && \
    echo "Creating writable /home/user directory for non-root users..." && \
    mkdir -p /home/user && \
    chmod 0777 /home/user && \
    echo "Cleaning up APT cache to keep the image small..." && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Ensure correct permissions for /home/user at runtime
RUN chmod 755 /home/user

# %environment section
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

# %help section
# This container provides the tooling required for the CPU-bound micro-benchmark
# exercise. Python and pytest are installed for automated validation, and a
# writable /home/user directory is pre-created so that non-root users can store
# their benchmark results at /home/user/benchmark/sha256_timing.csv.