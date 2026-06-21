FROM ubuntu:22.04

# Update package index and install Python plus essential tooling
RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        python3-venv \
        ca-certificates \
        git \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Install pytest for the verification framework
RUN python3 -m pip install --no-cache-dir pytest

# Create the backup directory structure and make it writable for any user
RUN mkdir -p /home/user/backups && \
    chmod -R 0777 /home/user

# Set environment variables
ENV PATH="/usr/local/bin:/usr/bin:/bin:$PATH"
ENV PYTHONIOENCODING=utf-8

# Set working directory
WORKDIR /home/user

# Default command
CMD echo "Container ready.  Use this shell to perform the backup/restore task." && /bin/bash