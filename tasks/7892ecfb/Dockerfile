# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# Updating package lists and installing prerequisites, installing pytest, and setting up /home/user
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip set -e && \
    echo "Updating package lists and installing prerequisites..." && \
    apt-get update -qq && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        ca-certificates \
        tzdata && \
    echo "Installing pytest via pip..." && \
    pip3 install --no-cache-dir --upgrade pip && \
    pip3 install --no-cache-dir pytest && \
    echo "Creating writable /home/user directory with open permissions..." && \
    mkdir -p /home/user && \
    chmod 0777 /home/user && \
    echo "Cleaning up APT caches..." && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

LABEL Author="Container setup for UTC timestamp logging task" \
      Purpose="Prepare initial state for learner—pytest installed, /home/user present"