# syntax=docker/dockerfile:1
# Based on a local image bootstrap, using the closest equivalent base
FROM ubuntu:22.04

# Help / label info
# Author: "Apptainer Build Script for Grafana Checksum Task"
LABEL Author="Apptainer Build Script for Grafana Checksum Task"

# Post section
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest && \
    mkdir -p /home/user/dashboards && \
    mkdir -p /home/user/verifications && \
    : > /home/user/dashboards/node_exporter.json && \
    echo "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  node_exporter.json" \
        > /home/user/dashboards/node_exporter.sha256 && \
    chmod -R a+rX /home/user && \
    chmod -R a+rw /home/user/verifications && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Environment section
ENV PATH="$PATH"
RUN chmod 755 /home/user

WORKDIR /home/user