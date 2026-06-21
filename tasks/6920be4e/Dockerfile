# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# Labels from Apptainer definition
LABEL Author="Apptainer Auto-Builder"
LABEL Description="Container for backup-restore timing exercise with pytest pre-installed"

# --- %post section ---
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked set -e && \
    echo "Updating apt and installing required packages..." && \
    apt-get update -y && \
    apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        tar \
        gzip \
        ca-certificates && \
    rm -rf /var/lib/apt/lists/*

RUN --mount=type=cache,target=/root/.cache/pip echo "Installing pytest via pip..." && \
    pip3 install --no-cache-dir pytest

RUN echo "Creating required directory structure and sample tarball..." && \
    mkdir -p /home/user/backups && \
    mkdir -p /home/user/restore_scratch && \
    WORKDIR=/tmp/app_config_sample && \
    mkdir -p "${WORKDIR}" && \
    echo "sample_key=sample_value" > "${WORKDIR}/config.ini" && \
    echo "<root><value>42</value></root>" > "${WORKDIR}/settings.xml" && \
    echo "#!/bin/sh\necho \"Hello, World!\"" > "${WORKDIR}/start.sh" && \
    chmod +x "${WORKDIR}/start.sh" && \
    tar -czf /home/user/backups/app_config_2024-06-01.tar.gz -C "${WORKDIR}" . && \
    rm -rf "${WORKDIR}" && \
    chmod 0755 /home/user && \
    chmod 0755 /home/user/backups && \
    chmod 0777 /home/user/restore_scratch && \
    echo "Container setup complete."

# --- %environment section ---
# Note: chmod commands from %environment are applied at build time above
ENV PYTHONIOENCODING=utf8
ENV PYTHONUSERBASE=/tmp/.python
ENV PATH=/tmp/.python/bin:$PATH

# --- %help section ---
# This container provides the initial state for the backup-restore
# performance-measurement exercise.
# Directories and files created:
#   • /home/user/backups/app_config_2024-06-01.tar.gz  (sample tarball)
#   • /home/user/restore_scratch                       (empty, writable)
# pytest is available for automated grading.