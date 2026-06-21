# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# Author backup-engineer-task
# Description "Environment for backup verification task with initial dataset"

RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

RUN adduser --disabled-password --gecos "" user

RUN install -d -m 0755 /home/user/project_data && \
    printf "The quick brown fox jumps over the lazy dog\n" > /home/user/project_data/data1.txt && \
    printf "Sphinx of black quartz, judge my vow\n" > /home/user/project_data/data2.txt && \
    printf "mode=production\n" > /home/user/project_data/config.cfg && \
    chmod 0644 /home/user/project_data/data1.txt /home/user/project_data/data2.txt /home/user/project_data/config.cfg && \
    chown -R user:user /home/user

RUN --mount=type=cache,target=/root/.cache/pip pip3 install --no-cache-dir pytest

ENV PATH=/usr/local/bin:/usr/bin:/bin:$PATH

RUN chmod 755 /home/user

# Apptainer runscript:
# Container for backup task. Switch to the 'user' account to begin.
# Example: sudo apptainer exec --writable-tmpfs <image>.sif bash
# (Inside the container, you will already be the invoking host user.)