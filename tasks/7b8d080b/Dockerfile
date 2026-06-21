# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# Author: Auto-generated for MLOps manifest exercise
# Description: Container providing initial state and pytest for distributed training artefact manifest task.

# This container sets up the initial directory structure and empty artefact
# files for the “distributed training manifest” exercise. Pytest is
# pre-installed so the automated grader can validate the environment.

RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip set -e && \
    apt-get update && \
    apt-get install -y --no-install-recommends python3 python3-pip && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Create user and home directory
RUN useradd -m -d /home/user user

# Prepare initial filesystem state for the distributed-training task
RUN set -e && \
    BASE_DIR="/home/user/distr_exp/run_42" && \
    mkdir -p "${BASE_DIR}/node01" "${BASE_DIR}/node02" && \
    touch \
        "${BASE_DIR}/node01/model.bin" \
        "${BASE_DIR}/node01/metrics.json" \
        "${BASE_DIR}/node02/model.bin" \
        "${BASE_DIR}/node02/metrics.json" && \
    chmod -R a+rwX /home/user/distr_exp

# Ensure permissions on home directory
RUN chmod 755 /home/user

LABEL Author="Auto-generated for MLOps manifest exercise" \
      Description="Container providing initial state and pytest for distributed training artefact manifest task."