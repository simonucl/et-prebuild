# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# Labels from Apptainer %labels section
LABEL Author="ChatGPT"
LABEL Description="Container for the API-summary shell-automation task with pytest pre-installed."

# Install Python, pip, and pytest
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip set -e && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        ca-certificates && \
    rm -rf /var/lib/apt/lists/* && \
    pip3 install --no-cache-dir pytest

# Prepare initial workspace expected by the grading tests
RUN set -e && \
    mkdir -p /home/user/mock_responses && \
    printf '{"service":"alpha","status":"ok"}' \
        > /home/user/mock_responses/status.json && \
    printf '{"requests":123,"errors":0,"uptime":"48h"}' \
        > /home/user/mock_responses/metrics.json && \
    chmod 644 /home/user/mock_responses/status.json \
              /home/user/mock_responses/metrics.json && \
    chmod 755 /home/user

# Environment variables from Apptainer %environment section
ENV PATH="/usr/local/bin:/usr/bin:/bin:$PATH"

# Default action: drop to a shell within the container
CMD ["/bin/bash"]