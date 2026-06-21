# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# Labels from Apptainer definition
LABEL Author="Apptainer build script" \
      Description="Environment for SQLite meta-information & summary report assignment"

# Basic system utilities and Python tooling
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3-pip \
        python3-setuptools \
        python3-wheel \
        sqlite3 \
        ca-certificates \
        curl && \
    rm -rf /var/lib/apt/lists/*

# Install pytest for the verification test-suite
RUN --mount=type=cache,target=/root/.cache/pip pip3 install --no-cache-dir pytest

# Ensure the expected directory structure exists
RUN mkdir -p /home/user/project

# Give write permissions to any unprivileged user who will run the container
RUN chmod 0777 /home/user && \
    chmod 0777 /home/user/project

# Guarantee that no pre-existing artefacts are present
RUN rm -f /home/user/project/meta.db || true && \
    rm -f /home/user/project/category_counts.log || true

# Environment setup
RUN chmod 755 /home/user
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8