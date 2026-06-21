# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# Updating package lists and installing required packages
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip set -e && \
    echo "Updating package lists..." && \
    apt-get update -y && \
    echo "Installing required packages..." && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        make \
        python3 \
        python3-pip && \
    echo "Installing pytest via pip..." && \
    pip3 install --no-cache-dir pytest && \
    echo "Creating expected home directory..." && \
    mkdir -p /home/user && \
    chmod 0777 /home/user && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Ensure correct permissions on home directory
RUN chmod 755 /home/user

# Environment variables
ENV PATH="/usr/local/bin:${PATH}"

# Labels
LABEL Author="Apptainer Build Automation" \
      Description="Environment prepared for compliance Makefile exercise, with pytest pre-installed."