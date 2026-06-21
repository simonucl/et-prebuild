# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# Install Python tooling and pytest
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip set -eux && \
    apt-get update && \
    apt-get install -y --no-install-recommends python3-pip && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Prepare filesystem
RUN mkdir -p /home/user/build && \
    chmod 755 /home/user && \
    chmod 755 /home/user/build

# Populate raw_artifacts.log
RUN cat > /home/user/build/raw_artifacts.log <<'EOF'
libfoo.so
libbar.so
libfoo.so
libbaz.so
libfoo.so
libbar.so
libqux.so
EOF

RUN chmod 644 /home/user/build/raw_artifacts.log

# Labels
LABEL Author="Auto-generated for artifact frequency task"
LABEL Description="Base image with pytest and initial data setup"