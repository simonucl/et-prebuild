# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# Help text from %help
# This Apptainer image contains the initial state and dependencies
# required to run the backup task along with pytest for validation.

LABEL Author="backup-task-setup"
LABEL Description="Container prepared for the SQL backup reliability task."

RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip set -e && \
    apt-get update && \
    apt-get install -y --no-install-recommends python3 python3-pip && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN mkdir -p /home/user/data && \
    chmod -R 0777 /home/user

RUN printf 'This is a sample PostgreSQL dump\n' > /home/user/data/dump.sql && \
    chmod 0666 /home/user/data/dump.sql