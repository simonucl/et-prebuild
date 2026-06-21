FROM ubuntu:22.04

# Install Python and pip
RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Upgrade pip and install pytest (needed for the grader)
RUN python3 -m pip install --no-cache-dir --upgrade pip && \
    python3 -m pip install --no-cache-dir pytest

# Prepare a consistent, writable cache location for pip expected by the tests
RUN mkdir -p /home/user/.cache/pip && \
    chmod -R 0777 /home/user

# Set environment variables
ENV PIP_CACHE_DIR=/home/user/.cache/pip

# Set entrypoint
ENTRYPOINT ["/bin/bash", "-c", "chmod 755 /home/user && exec \"$@\"", "--"]