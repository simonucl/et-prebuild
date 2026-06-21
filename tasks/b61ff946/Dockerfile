# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# %post
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip set -eux && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends python3 python3-pip && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN set -eux && \
    mkdir -p /home/user/project_data && \
    mkdir -p /home/user/backup/project_data_copy && \
    printf 'abc'  > /home/user/project_data/data1.txt && \
    printf 'test' > /home/user/project_data/data2.txt && \
    cp /home/user/project_data/data1.txt /home/user/backup/project_data_copy/ && \
    cp /home/user/project_data/data2.txt /home/user/backup/project_data_copy/ && \
    chmod 0777 /home/user && \
    chmod -R a+rX /home/user/project_data /home/user/backup

# %environment
RUN chmod 755 /home/user
ENV PATH="/usr/local/bin:$PATH"

# %labels
LABEL Author="backup-integrity-exercise"
LABEL Description="Initial state for the backup verification task"