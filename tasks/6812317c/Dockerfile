# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# --------------------------------------------------
# Author label
# --------------------------------------------------
LABEL Author="Container prepared for artifact size summarization task"

# --------------------------------------------------
# Install Python, pip, and pytest
# --------------------------------------------------
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip set -e && \
    apt-get update && \
    apt-get install -y --no-install-recommends python3 python3-pip && \
    pip3 install --no-cache-dir pytest && \
    rm -rf /var/lib/apt/lists/*

# --------------------------------------------------
# Create the expected UNIX user and home directory
# --------------------------------------------------
RUN useradd -m -s /bin/bash user || true

# --------------------------------------------------
# Prepare the initial experiment directory and contents
# --------------------------------------------------
RUN set -e && \
    EXP_DIR="/home/user/experiments/run_03" && \
    mkdir -p "${EXP_DIR}" && \
    chmod 777 "${EXP_DIR}" && \
    printf 'DUMMY_MODEL_CONTENT\n' > "${EXP_DIR}/model.pt" && \
    printf '{"accuracy": 0.92, "loss": 0.15}\n' > "${EXP_DIR}/metrics.json" && \
    printf 'batch_size: 32\nlearning_rate: 0.001\n' > "${EXP_DIR}/config.yaml" && \
    printf 'Epoch,Loss,Accuracy\n1,0.45,0.78\n2,0.32,0.84\n3,0.21,0.88\n' > "${EXP_DIR}/training.log" && \
    chmod 644 "${EXP_DIR}"/*

# --------------------------------------------------
# Environment setup
# --------------------------------------------------
RUN chmod 755 /home/user

ENV PYTHONUNBUFFERED=1

# --------------------------------------------------
# Help
# Container prepared for artifact size summarization task
# --------------------------------------------------