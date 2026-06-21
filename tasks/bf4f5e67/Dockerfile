# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# Update package index and install Python + pip
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked apt-get update && \
    apt-get install -y --no-install-recommends python3 python3-pip && \
    rm -rf /var/lib/apt/lists/*

# Install pytest for the grading tests
RUN --mount=type=cache,target=/root/.cache/pip pip3 install --no-cache-dir pytest

# Create a non-privileged user `user` and its HOME
RUN groupadd -g 1000 user || true && \
    useradd -m -u 1000 -g 1000 -d /home/user user || true

# Pre-stage workspace
RUN mkdir -p /home/user/project/scripts && \
    mkdir -p /home/user/project/data

# Files with placeholder content
RUN echo "# sample config" > /home/user/project/config.cfg
RUN echo -e "#!/bin/bash\necho Building…" > /home/user/project/scripts/build.sh
RUN echo "raw data" > /home/user/project/data/raw.txt

# Set permissions
RUN chmod 0755 /home/user/project && \
    chmod 0644 /home/user/project/config.cfg && \
    chmod 0755 /home/user/project/scripts && \
    chmod 0750 /home/user/project/scripts/build.sh && \
    chmod 0700 /home/user/project/data && \
    chmod 0600 /home/user/project/data/raw.txt

# Ensure ownership
RUN chown -R 1000:1000 /home/user

# Apply environment-time chmod
RUN chmod 755 /home/user

# Environment variables
ENV LC_ALL=C
ENV LANG=C

# Run script equivalent
CMD ["bash", "-c", "exec \"$@\"", "--"]