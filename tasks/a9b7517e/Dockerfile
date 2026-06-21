# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# Update package index and install Python + pip
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        coreutils && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install pytest
RUN --mount=type=cache,target=/root/.cache/pip pip3 install --no-cache-dir pytest

# Create non-root user `user` with UID 1000
RUN useradd -m -s /bin/bash -u 1000 user

# Prepare initial filesystem state
RUN mkdir -p /home/user/builds && \
    printf 'hello' > /home/user/builds/webapp_2023-09-15.tar.gz && \
    chmod 0644 /home/user/builds/webapp_2023-09-15.tar.gz && \
    chown -R 1000:1000 /home/user

# Environment setup
RUN chmod 755 /home/user
ENV PATH=/usr/local/bin:/usr/bin:/bin

# Default command
CMD ["/bin/bash"]