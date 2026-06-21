# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# Labels from Apptainer definition
LABEL Author="YourName" \
      Purpose="Container for the init-PID audit assignment"

# Basic utilities, Python, pytest, and user setup
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip set -e && \
    export DEBIAN_FRONTEND=noninteractive && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        ca-certificates && \
    pip3 install --no-cache-dir pytest && \
    groupadd -g 1000 user && \
    useradd -m -u 1000 -g 1000 -s /bin/bash user && \
    chown -R 1000:1000 /home/user && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Ensure home directory permissions
RUN chmod 755 /home/user

# Environment variables
ENV LANG=C.UTF-8 \
    LC_ALL=C.UTF-8 \
    PATH=/usr/local/bin:/usr/bin:/bin:$PATH

# Switch to non-root user
USER user
WORKDIR /home/user

# Equivalent of Apptainer runscript
CMD sh -c 'echo "This container is ready for the init-PID audit assignment." && echo "Open a shell with:  docker run -it <image> /bin/bash" && exec /bin/bash'