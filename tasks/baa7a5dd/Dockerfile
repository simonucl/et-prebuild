# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# Update package list and install required software
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked apt-get update && \
    apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        sqlite3 && \
    rm -rf /var/lib/apt/lists/*

# Install pytest for the exercise test-suite
RUN --mount=type=cache,target=/root/.cache/pip pip3 install --no-cache-dir pytest

# Ensure the base working directory exists for the student
RUN mkdir -p /home/user && chmod 755 /home/user

# Basic locale settings
ENV LANG=C
ENV LC_ALL=C

# Labels
LABEL Author="QA_Assistant"
LABEL Description="Environment for SQLite migration exercise (pytest included)"