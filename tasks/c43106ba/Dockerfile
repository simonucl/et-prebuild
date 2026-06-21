# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# Update apt index and install Python & pip
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked apt-get update -y && \
    apt-get install -y --no-install-recommends python3-pip && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install pytest for the grader
RUN --mount=type=cache,target=/root/.cache/pip pip3 install --no-cache-dir pytest

# Prepare initial project structure
RUN mkdir -p /home/user/project/config

# model_config.yaml
RUN cat <<'EOF' > /home/user/project/config/model_config.yaml
dataset:
  path: "/data/train.csv"
  batch_size: 32
  shuffle: true
EOF

# run_settings.toml
RUN cat <<'EOF' > /home/user/project/config/run_settings.toml
[run]
epochs = 10
learning_rate = 0.001
EOF

# Ensure permissions
RUN chmod -R a+rwx /home/user/project && chmod 755 /home/user

# Environment variables
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

# Labels
LABEL Author="someone@example.com"
LABEL Description="Container for configuration-editing single-command exercise"