# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# Install Python and pytest
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        procps && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Prepare writable home for the exercise participant
RUN mkdir -p /home/user && chmod 0777 /home/user

# Apply extra permission from labels section
RUN chmod 755 /home/user

# Metadata
LABEL Author="DeploymentExercise"
LABEL Description="Base image for the deployment-logs task with pytest pre-installed."

# Environment variables
ENV PATH="/usr/local/bin:/usr/bin:/bin:${PATH}"