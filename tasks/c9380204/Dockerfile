# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# Labels from Apptainer
LABEL Maintainer="Apptainer task setup"
LABEL Description="Environment prepared for inventory conversion exercise"

# Install packages
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        python3-setuptools \
        python3-wheel && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install pytest
RUN --mount=type=cache,target=/root/.cache/pip pip3 install --no-cache-dir pytest

# Create directory structure
RUN mkdir -p /home/user/build

# Create seeded inventory.csv file
RUN cat >/home/user/build/inventory.csv <<'EOF'
artifact,version,sha256
core-lib,1.2.3,abc123def456
ui-module,2.0.0-rc1,789abc012def
cli-tool,0.9.8,fedcba987654
EOF

# Set permissions
RUN chmod 777 /home/user/build && \
    chmod 755 /home/user && \
    chmod 644 /home/user/build/inventory.csv

# Environment block (kept empty as in Apptainer)
ENV HOME=/home/user

# Default command similar to %runscript
CMD ["/bin/bash"]