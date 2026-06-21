# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# From %help and %labels
LABEL Author="Apptainer Task Builder"
LABEL Description="Base image for capacity-planner exercise with pytest pre-installed."
# Run script equivalent:
# Capacity-planner exercise container.
# Start a shell with: apptainer exec -e $0 /bin/bash

RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends python3 python3-pip && \
    pip3 install --no-cache-dir pytest && \
    rm -rf /var/lib/apt/lists/*

RUN mkdir -p /home/user/reports && \
    chmod 0777 /home/user && \
    chmod 0777 /home/user/reports

RUN chmod 755 /home/user

ENV PATH=/usr/local/bin:/usr/bin:/bin:$PATH