# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# Labels
LABEL Author="Apptainer Task Prep"
LABEL Description="Container for ML data backup CI exercise with pytest pre-installed."

# Environment variables
ENV PATH=/usr/local/bin:/usr/local/sbin:/usr/sbin:/usr/bin:/sbin:/bin

RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked set -e && \
    apt-get update -y && \
    apt-get install -y --no-install-recommends python3 python3-pip && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN --mount=type=cache,target=/root/.cache/pip pip3 install --no-cache-dir pytest

RUN mkdir -p /home/user/ml_data/train && \
    mkdir -p /home/user/backups

RUN cat << 'EOF' > /home/user/ml_data/train/features.csv
f1,f2,f3
1,2,3
4,5,6
EOF

RUN cat << 'EOF' > /home/user/ml_data/train/targets.csv
t
0
1
EOF

RUN chmod 755 /home/user && \
    chmod 755 /home/user/ml_data /home/user/ml_data/train && \
    chmod 777 /home/user/backups && \
    chmod 644 /home/user/ml_data/train/features.csv && \
    chmod 644 /home/user/ml_data/train/targets.csv