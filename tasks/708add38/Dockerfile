# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# -----------------------------------------------------------------
# Basic development tools
# -----------------------------------------------------------------
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked set -e && \
    apt-get update && \
    apt-get install -y --no-install-recommends python3 python3-pip && \
    rm -rf /var/lib/apt/lists/*

# Python testing framework
RUN --mount=type=cache,target=/root/.cache/pip pip3 install --no-cache-dir pytest

# -----------------------------------------------------------------
# Prepare the required filesystem hierarchy for the exercise
# -----------------------------------------------------------------
RUN set -e && \
    mkdir -p /home/user && \
    mkdir -p /home/user/microservices && \
    chmod 0777 /home/user/microservices && \
    mkdir -p /home/user/microservices/auth-service-1.2.3 && \
    mkdir -p /home/user/microservices/billing-service-2.4.0 && \
    chmod 755 /home/user

# -----------------------------------------------------------------
# Environment settings
# -----------------------------------------------------------------
ENV PATH=/usr/local/bin:/usr/bin:/bin:$PATH

# -----------------------------------------------------------------
# Metadata
# -----------------------------------------------------------------
LABEL Author="Microservices Exercise Image" \
      Description="Sets up initial directories for symlink/report task"