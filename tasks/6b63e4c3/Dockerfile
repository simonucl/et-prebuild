# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# ------------------------------------------------------------------
# Base system packages and setup
# ------------------------------------------------------------------
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked set -eux && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        ca-certificates && \
    rm -rf /var/lib/apt/lists/*

# ------------------------------------------------------------------
# Python testing utilities
# ------------------------------------------------------------------
RUN --mount=type=cache,target=/root/.cache/pip pip3 install --no-cache-dir pytest pytest-order

# ------------------------------------------------------------------
# Create the non-privileged user that the grading agent will use
# ------------------------------------------------------------------
RUN groupadd -g 1000 user && \
    useradd -m -u 1000 -g 1000 user

# ------------------------------------------------------------------
# Prepare the required initial filesystem layout
# ------------------------------------------------------------------
RUN mkdir -p /home/user/data_pipeline/logs && \
    : > /home/user/data_pipeline/config.yaml && \
    chmod 0755 /home/user && \
    chmod 0755 /home/user/data_pipeline && \
    chmod 0755 /home/user/data_pipeline/logs && \
    chmod 0644 /home/user/data_pipeline/config.yaml && \
    chown -R user:user /home/user

# ------------------------------------------------------------------
# Environment variables
# ------------------------------------------------------------------
ENV PYTHONUNBUFFERED=1
ENV PATH=/usr/local/bin:/usr/bin:/bin:$PATH

# ------------------------------------------------------------------
# Metadata labels
# ------------------------------------------------------------------
LABEL Author="container-build system"
LABEL Description="Environment for the audit-trail configuration task (pytest included)"

# ------------------------------------------------------------------
# Default command: start a shell as the non-privileged user
# ------------------------------------------------------------------
USER user
WORKDIR /home/user
CMD ["/bin/bash"]