# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# ------------------------------------------------------------------
# Author: incident-response-exercise
# Description: Container for incident-response checksum exercise
#
# This container sets up the initial state for the incident-response
# checksum exercise. The evidence directory and the suspicious binary
# are pre-created so that students can calculate and log its SHA-256
# digest as instructed.
# ------------------------------------------------------------------

RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        ca-certificates \
        coreutils && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install pytest for the grading framework
RUN --mount=type=cache,target=/root/.cache/pip pip3 install --no-cache-dir pytest

# Prepare initial evidence directory and files expected by the tests
RUN mkdir -p /home/user && \
    mkdir -p /home/user/evidence && \
    chmod 755 /home/user/evidence && \
    : > /home/user/evidence/suspicious.bin && \
    chmod 644 /home/user/evidence/suspicious.bin