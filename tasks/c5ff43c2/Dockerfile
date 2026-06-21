# syntax=docker/dockerfile:1
# Converted from Apptainer definition file
FROM ubuntu:22.04

# Environment variables
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

# Install packages and pytest
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip set -eu && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        curl \
        ca-certificates && \
    rm -rf /var/lib/apt/lists/* && \
    pip3 install --no-cache-dir pytest

# Prepare writable home directory
RUN mkdir -p /home/user && chmod 0777 /home/user

# Equivalent of %runscript message (Docker advises CMD)
CMD chmod 755 /home/user && \
    echo "Apptainer container for the emergency static site exercise." && \
    echo "Launch a shell and follow the task instructions."