FROM ubuntu:22.04

# Update package lists and install Python tooling for pytest
RUN set -e && \
    apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends python3-pip && \
    pip3 install --no-cache-dir pytest

# Prepare writable home for the non-root user
RUN mkdir -p /home/user && \
    chmod 777 /home/user && \
    touch /home/user/.bashrc && \
    chmod 666 /home/user/.bashrc

# Clean up apt caches
RUN apt-get clean && rm -rf /var/lib/apt/lists/*

# Apply permission from environment section
RUN chmod 755 /home/user

ENV PATH="$PATH:/root/.local/bin"

CMD ["/bin/bash"]