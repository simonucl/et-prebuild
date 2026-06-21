# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# Author="Apptainer Build Script"
# Description="Base image for compliance-lab exercise; contains Python, pytest, sqlite3, and an empty /home/user directory."

ENV DEBIAN_FRONTEND=noninteractive
ENV PATH=/usr/local/bin:/usr/bin:/bin:$PATH

RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip set -e && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        python3-setuptools \
        sqlite3 \
        ca-certificates && \
    pip3 install --no-cache-dir --upgrade pip && \
    pip3 install --no-cache-dir pytest && \
    mkdir -p /home/user && \
    chmod 0777 /home/user && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN chmod 755 /home/user