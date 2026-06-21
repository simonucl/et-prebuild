FROM ubuntu:22.04

# Labels
LABEL Author="Symlink-Exercise Setup"
LABEL Description="Environment pre-configured for the datasets symbolic-link task."

# Basic tooling
RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        ca-certificates \
        git && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN pip3 install --no-cache-dir pytest

# Filesystem layout for the exercise
# Create the directory tree that must already exist when the student starts.
RUN mkdir -p /home/user/datasets/raw/experiment_A && \
    mkdir -p /home/user/datasets/raw/experiment_B && \
    mkdir -p /home/user/datasets/processed/experiment_A_clean && \
    mkdir -p /home/user/datasets/processed/experiment_B_clean && \
    mkdir -p /home/user/datasets/archive

# Pre-existing broken symlink (must be dangling).
RUN ln -sf ../raw/missing_experiment /home/user/datasets/archive/exp_old

# Ensure everything under /home/user is writable by the unprivileged user
# who will run inside the container.
RUN chmod -R a+rwx /home/user

# Environment variables
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /home/user