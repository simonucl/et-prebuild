# syntax=docker/dockerfile:1
# Converted from Apptainer definition
FROM ubuntu:22.04

# Environment variables (none provided in %environment)

# ----- System setup -----
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked set -e && \
    apt-get update && \
    apt-get install -y --no-install-recommends python3 python3-pip ca-certificates && \
    rm -rf /var/lib/apt/lists/*

RUN --mount=type=cache,target=/root/.cache/pip pip3 install --no-cache-dir pytest

# ----- Create directory structure -----
RUN mkdir -p /home/user/datasets

# ----- Populate data file -----
RUN cat > /home/user/datasets/measurements_2023.txt <<'EOF'
EXP001 23.4 2023-05-01
EXP002 19.8 2023-05-02
EXP003 25.1 2023-05-03
EXP004 21.0 2023-05-04
EXP005 20.7 2023-05-05
EOF

# ----- Set permissions -----
RUN chmod 777 /home/user && \
    chmod 777 /home/user/datasets && \
    chmod 644 /home/user/datasets/measurements_2023.txt

# ----- Labels -----
LABEL Author="YourName"
LABEL Description="Environment for the laboratory readings standardisation task"