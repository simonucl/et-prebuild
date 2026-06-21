FROM ubuntu:22.04

# Basic tooling
RUN set -e && \
    apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        ca-certificates \
        tzdata && \
    rm -rf /var/lib/apt/lists/* && \
    pip3 install --no-cache-dir pytest

# Create non-root user “user”
RUN useradd -m -s /bin/bash user || true && \
    mkdir -p /home/user && \
    chown -R user:user /home/user

# Construct initial experiment directory tree & files
RUN set -e && \
    EXP_BASE="/home/user/experiments" && \
    mkdir -p "${EXP_BASE}" && \
    RUN1="${EXP_BASE}/run_2023-08-01" && \
    mkdir -p "${RUN1}/logs" && \
    printf 'Epoch 1: loss 0.123\n' > "${RUN1}/logs/train.log" && \
    printf 'Val accuracy 0.95\n' > "${RUN1}/logs/val.log" && \
    printf '{"loss": 0.123, "accuracy": 0.95}\n' > "${RUN1}/metrics.json" && \
    printf 'CKPT1' > "${RUN1}/model_epoch=01.ckpt" && \
    printf 'CKPT2' > "${RUN1}/model_epoch=02.ckpt" && \
    RUN2="${EXP_BASE}/run_2023-08-02" && \
    mkdir -p "${RUN2}/logs" && \
    printf 'Epoch 1: loss 0.321\n' > "${RUN2}/logs/train.log" && \
    printf 'Val accuracy 0.90\n' > "${RUN2}/logs/val.log" && \
    printf '{"loss": 0.321, "accuracy": 0.90}\n' > "${RUN2}/metrics.json" && \
    printf 'CKPT3' > "${RUN2}/model_epoch=03.ckpt" && \
    printf 'CKPT4' > "${RUN2}/model_epoch=04.ckpt" && \
    RUN3="${EXP_BASE}/run_2023-08-03" && \
    mkdir -p "${RUN3}/logs" && \
    printf 'Epoch 1: loss 0.555\n' > "${RUN3}/logs/train.log" && \
    printf 'Val accuracy 0.88\n' > "${RUN3}/logs/val.log" && \
    chmod -R a+rwX /home/user && \
    chown -R user:user /home/user

# Environment
RUN chmod 755 /home/user
ENV PATH="/home/user/.local/bin:${PATH}"

LABEL Author="MLOps-Setup"
LABEL Description="Initial state container for checkpoint-archiving exercise"

CMD bash -c "echo 'Container built for the checkpoint-archiving exercise.' && echo 'Switch to /home/user/experiments and begin your work.'"