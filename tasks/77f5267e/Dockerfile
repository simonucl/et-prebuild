# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# ---- %help ----
# This Apptainer image sets up the initial state for the
# “symbolic-link integrity” exercise.
# Pre-installed: Python 3 + pytest.
# Pre-created:
#   • /home/user/data/live/important.db
#   • /home/user/archives/snap_latest  (broken symlink -> /home/user/data/old_live)
# Students will repair and validate the links as described in the task.

RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip set -e && \
    apt-get update -qq && \
    apt-get install -y --no-install-recommends python3 python3-pip && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN set -e && \
    mkdir -p /home/user && \
    mkdir -p /home/user/data/live && \
    : > /home/user/data/live/important.db && \
    mkdir -p /home/user/archives && \
    ln -sf /home/user/data/old_live /home/user/archives/snap_latest && \
    chmod -R a+rwX /home/user

RUN chmod 755 /home/user

LABEL Author="Backup-Integrity Exercise"