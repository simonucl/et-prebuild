# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# Labels from Apptainer definition
LABEL Author="IoT-Gateway Task Prep" \
      Description="Base image for edge-computing health-check exercise"

# Post section commands
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3-pip \
        iputils-ping \
        ca-certificates && \
    rm -rf /var/lib/apt/lists/*

# Install pytest for the test harness
RUN --mount=type=cache,target=/root/.cache/pip pip3 install --no-cache-dir pytest

# Create the expected user directory and helper file
RUN mkdir -p /home/user && \
    echo "198.51.100.42" > /home/user/iot_gateway_ip.txt && \
    chmod 755 /home/user && \
    chmod 644 /home/user/iot_gateway_ip.txt

# Help:
# Base image for edge-computing health-check exercise using Ubuntu 22.04