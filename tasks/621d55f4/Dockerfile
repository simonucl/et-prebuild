# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# Labels converted from %labels
LABEL Author="ChatGPT" \
      Description="Container for CSV counting task: sets up /home/user/data/raw with three CSV files and installs pytest."

# Post section converted to RUN commands
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    rm -rf /var/lib/apt/lists/*

# Install pytest for the grading suite
RUN --mount=type=cache,target=/root/.cache/pip pip3 install --no-cache-dir pytest

# Create home directory, required directory structure, and CSV seed files
RUN mkdir -p /home/user/data/raw && \
    printf 'id,amount\n' > /home/user/data/raw/sales_north.csv && \
    printf 'id,amount\n' > /home/user/data/raw/sales_south.csv && \
    printf 'id,amount\n' > /home/user/data/raw/sales_west.csv && \
    chmod -R 777 /home/user/data && \
    chmod 755 /home/user

# Environment section converted to ENV
ENV PATH=/usr/local/bin:/usr/bin:/bin