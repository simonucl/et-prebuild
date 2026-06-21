# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# Author="chatGPT"
# Description="Container providing the initial state for the release-manager deployment task"

RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip set -e && \
    apt-get update && \
    apt-get install -y --no-install-recommends python3-pip && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN id -u user >/dev/null 2>&1 || useradd -m -u 1000 user

RUN DEPLOY_DIR="/home/user/deployment" && \
    RELEASES_DIR="${DEPLOY_DIR}/releases" && \
    mkdir -p "${RELEASES_DIR}/v1.0.0" && \
    mkdir -p "${RELEASES_DIR}/v1.1.0" && \
    ln -sf "${RELEASES_DIR}/v1.1.0" "${DEPLOY_DIR}/current" && \
    : > "${DEPLOY_DIR}/deploy.log"

RUN chown -R 1000:1000 /home/user

RUN chmod 755 /home/user

ENV PATH="/home/user/.local/bin:${PATH}"

LABEL Author="chatGPT"
LABEL Description="Container providing the initial state for the release-manager deployment task"