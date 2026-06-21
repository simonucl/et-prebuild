# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# Install Python and pytest
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip set -e && \
    apt-get update && \
    apt-get install -y --no-install-recommends python3 python3-pip && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Create project directory and placeholder source file
RUN mkdir -p /home/user/project/src

RUN cat <<'EOF' >/home/user/project/src/app.py
# sample source file
print("Hello from project")
EOF

# Ensure non-root can create /home/user/release
RUN chmod -R 0777 /home/user

# From %environment section
RUN chmod 755 /home/user
ENV PYTHONUNBUFFERED=1