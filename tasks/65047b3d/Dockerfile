# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# Labels from Apptainer definition
LABEL Author="Apptainer Build System"
LABEL Description="Base image for the exp1 virtual-environment exercise. Pytest pre-installed."

# Post section: install dependencies and pytest
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked set -e && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
        python3 \
        python3-venv \
        python3-pip && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install pytest (required by the automated tests)
RUN --mount=type=cache,target=/root/.cache/pip pip3 install --no-cache-dir pytest

# Create a writable home directory for the future “user” account
RUN mkdir -p /home/user && \
    chmod 0777 /home/user

# Environment setup (from %environment)
RUN chmod 755 /home/user
ENV HOME=/home/user
ENV PATH="$HOME/.local/bin:$PATH"

# Default command (approximation of %runscript behavior)
CMD ["/bin/bash"]