# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# Author="Container build automation"
# Description="Clean environment for the build-artifacts SQLite/CSV task with pytest and sqlite3 pre-installed."

LABEL Author="Container build automation" \
      Description="Clean environment for the build-artifacts SQLite/CSV task with pytest and sqlite3 pre-installed."

RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        sqlite3 && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* && \
    mkdir -p /home/user && \
    chmod 755 /home/user

ENV PATH=/usr/local/bin:/usr/bin:/bin
ENV HOME=/home/user