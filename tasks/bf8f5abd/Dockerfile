# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# Help text
# This Apptainer image contains the prepared directory structure for the
# edge_app OTA deployment exercise and has pytest installed for automated
# grading.

LABEL Author="edge_container_build_system"
LABEL Description="Initial state for OTA upgrade task with pytest pre-installed."

ENV HOME=/home/user

RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip set -e && \
    echo "Updating package index and installing Python tooling..." && \
    apt-get update -qq && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        ca-certificates && \
    echo "Installing pytest for internal test execution..." && \
    pip3 install --no-cache-dir pytest && \
    echo "Creating initial filesystem state for the edge_app releases..." && \
    mkdir -p /home/user && \
    mkdir -p /home/user/edge_app/releases/v1.2.0 && \
    mkdir -p /home/user/edge_app/releases/v1.2.1 && \
    printf "v1.2.0 build completed\n" > /home/user/edge_app/releases/v1.2.0/build.txt && \
    printf "v1.2.1 build completed\n" > /home/user/edge_app/releases/v1.2.1/build.txt && \
    ln -s /home/user/edge_app/releases/v1.2.0 /home/user/edge_app/current && \
    echo "Adjusting permissions so the non-root agent can modify needed paths..." && \
    chmod 777 /home/user && \
    chmod 777 /home/user/edge_app && \
    find /home/user/edge_app -type d -exec chmod 755 {} \; && \
    find /home/user/edge_app -type f -exec chmod 644 {} \;