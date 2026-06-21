# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# Help:
# This container provides the base environment for the “server_configs” task.
# All required assignment files are intentionally absent so that students can
# create them during the exercise. Pytest is installed for automated grading.

LABEL Author="Apptainer build for server_configs task"
LABEL Description="Clean environment with pytest installed and no pre-created deliverables."

ENV HOME=/home/user

RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest && \
    mkdir -p /home/user && \
    chmod 0777 /home/user && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN chmod 755 /home/user

CMD ["/bin/bash"]