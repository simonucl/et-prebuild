# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# Install Python, pip, and pytest
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip set -eux \
    && apt-get update \
    && apt-get install -y --no-install-recommends python3 python3-pip \
    && pip install --no-cache-dir pytest \
    && rm -rf /var/lib/apt/lists/*

# Set up initial filesystem expected by the tests
RUN mkdir -p /home/user/db
RUN echo "SELECT 1;" > /home/user/db/improved_query.sql
RUN chmod -R a+rwx /home/user

# Environment setup
RUN chmod 755 /home/user

LABEL Author="ChatGPT"
LABEL Description="Container for move-and-log SQL file task – includes pytest and initial directory layout."