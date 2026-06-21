# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# Install Python, pip, pytest, and clean up
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Create home directory
RUN mkdir -p /home/user

# Prepare experiment logs directory
RUN mkdir -p /home/user/experiments

# log1.txt
RUN cat > /home/user/experiments/log1.txt << 'EOF'
model_v1.ckpt
dataset_v1.zip
model_v1.ckpt
metrics_v1.json
dataset_v1.zip
EOF

# log2.txt
RUN cat > /home/user/experiments/log2.txt << 'EOF'
model_v2.ckpt
dataset_v1.zip
model_v1.ckpt
metrics_v1.json
metrics_v1.json
model_v2.ckpt
EOF

# Permissions
RUN chmod 0777 /home/user/experiments && \
    chmod 0644 /home/user/experiments/log1.txt /home/user/experiments/log2.txt && \
    chmod 755 /home/user

# Environment variables
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8