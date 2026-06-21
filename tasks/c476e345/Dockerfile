# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# Help / metadata
LABEL Author="Apptainer Exercise – Data Cleanup"
LABEL Description="Provides the initial messy CSV dataset plus pytest for validation."

# From %labels section (non‑label command)
RUN chmod 755 /home/user || true

# Basic tooling: Python + PyPI pytest
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip set -e && \
    apt-get update && \
    apt-get install -y --no-install-recommends python3 python3-pip && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Create the initial dataset directories
RUN mkdir -p /home/user/projects/data/raw/2020 && \
    mkdir -p /home/user/projects/data/raw/2021 && \
    mkdir -p /home/user/projects/data/raw/2022

# 2020 dataset
RUN cat <<'EOF' > /home/user/projects/data/raw/2020/q1_sales.csv
id,amount
1,100
2,200
EOF
RUN cp /home/user/projects/data/raw/2020/q1_sales.csv /home/user/projects/data/raw/2020/q1_sales.csv.bak && \
    touch /home/user/projects/data/raw/2020/empty.csv && \
    echo "2020 quarterly sales figures. Internal use only." > /home/user/projects/data/raw/2020/README.txt

# 2021 dataset
RUN cat <<'EOF' > /home/user/projects/data/raw/2021/q2_sales.csv
id,amount
3,300
4,400
EOF
RUN cp /home/user/projects/data/raw/2021/q2_sales.csv /home/user/projects/data/raw/2021/q2_sales.csv.bak && \
    touch /home/user/projects/data/raw/2021/empty.csv && \
    echo "secret note" > /home/user/projects/data/raw/2021/.hidden

# 2022 dataset
RUN cat <<'EOF' > /home/user/projects/data/raw/2022/q3_sales.csv
id,amount
5,500
6,600
EOF
RUN cp /home/user/projects/data/raw/2022/q3_sales.csv /home/user/projects/data/raw/2022/q3_sales.csv.bak && \
    touch /home/user/projects/data/raw/2022/empty.csv

# Permissions
RUN chmod -R a+rX /home/user && \
    find /home/user/projects -type d -exec chmod a+rwx {} +