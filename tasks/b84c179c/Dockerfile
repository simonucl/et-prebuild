# syntax=docker/dockerfile:1
# This container supplies a minimal Ubuntu 22.04 environment with pytest pre-installed.
# No task artefacts are present so that the learner can create them during the exercise.

FROM ubuntu:22.04

ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip set -e && \
    apt-get update && \
    apt-get install -y --no-install-recommends python3 python3-pip && \
    pip3 install --no-cache-dir pytest && \
    mkdir -p /home/user && \
    chmod 0777 /home/user && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN chmod 755 /home/user

# Equivalent of runscript:
# echo "Container for timezone task."
# echo "Run your commands or tests as needed."