# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# Labels from %labels
LABEL Author="Course Automation" \
      Version="1.0" \
      Description="Base image for the daily compressed backup exercise with pytest pre-installed."

# Update package index and install required software
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 python3-pip cron tar && \
    pip install --no-cache-dir pytest && \
    useradd -m -s /bin/bash user && \
    install -d -m 755 /home/user/datasets/raw && \
    install -d -m 755 /home/user/datasets/backups && \
    chown -R user:user /home/user/datasets && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Ensure correct permissions on home directory
RUN chmod 755 /home/user

# Environment variables from %environment
ENV PYTHONUNBUFFERED=1

# %help
# Base image for the daily compressed backup exercise with pytest pre-installed.
# Includes a non-privileged 'user' with datasets directory structure prepared.