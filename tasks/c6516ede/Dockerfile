# syntax=docker/dockerfile:1
# Converted from Apptainer definition
FROM ubuntu:22.04

# Environment variables
ENV DEBIAN_FRONTEND=noninteractive

# Install Python and pytest
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip apt-get update && \
    apt-get install -y --no-install-recommends python3 python3-pip && \
    pip3 install --no-cache-dir pytest && \
    rm -rf /var/lib/apt/lists/*

# Create directory structure
RUN mkdir -p /home/user/mobile_pipelines

# Populate build_targets.txt via heredoc
RUN cat <<'EOF' > /home/user/mobile_pipelines/build_targets.txt
android-29
android-30
ios-13
ios-14
android-31
ios-15
EOF

# Set permissions
RUN chmod 755 /home/user && \
    chmod 755 /home/user/mobile_pipelines && \
    chmod 644 /home/user/mobile_pipelines/build_targets.txt

# Metadata
# Author: Mobile-Pipeline-Setup
# Description: Base image with initial state and pytest installed.

# Run script equivalent
CMD ["bash"]