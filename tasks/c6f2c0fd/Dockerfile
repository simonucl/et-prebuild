# syntax=docker/dockerfile:1
# Converted from Apptainer definition file
FROM ubuntu:22.04

# Update package index and install Python + pip
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked apt-get update && \
    apt-get install -y --no-install-recommends python3 python3-pip && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Install pytest
RUN --mount=type=cache,target=/root/.cache/pip pip3 install --no-cache-dir pytest

# Create home directory
RUN mkdir -p /home/user && chmod 0777 /home/user

# Create sample_payloads directory and JSON files
RUN mkdir -p /home/user/sample_payloads

RUN printf '{"user":{"id":0,"name":"Alice"}}\n' \
    > /home/user/sample_payloads/user_create.json

RUN printf '{"order":{"id":0,"item":"Widget","quantity":3}}\n' \
    > /home/user/sample_payloads/order_create.json

# Set file permissions
RUN chmod 644 /home/user/sample_payloads/*.json

# Labels (converted as comments)
# Author chatbot
# Description: Container for API test-organising exercise – provides initial state and pytest