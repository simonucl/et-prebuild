# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# Update package lists and install Python tooling
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked apt-get update && \
    apt-get install -y --no-install-recommends \
        python3 \
        python3-venv \
        python3-pip && \
    rm -rf /var/lib/apt/lists/*

# Install pytest for the grader
RUN --mount=type=cache,target=/root/.cache/pip pip3 install --no-cache-dir pytest

# Create a standard, non-root user (UID 1000) expected by the tests
RUN groupadd -g 1000 user && \
    useradd -m -u 1000 -g user user

# Ensure the home directory exists and is writable
RUN mkdir -p /home/user && \
    chown -R 1000:1000 /home/user && \
    chmod 755 /home/user

# Add the local user’s bin directory to PATH for convenience
ENV PATH="/home/user/.local/bin:${PATH}"

# Default command when the container is executed
CMD ["/bin/bash"]