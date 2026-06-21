# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# Labels from Apptainer definition
LABEL Author="observability-container" \
      Description="Base image for the Observability Docs assignment with pytest installed."

# Post section: install packages, pytest, create user and home directory
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip set -e && \
    apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        grep \
        ca-certificates \
        curl \
        less && \
    pip3 install --no-cache-dir pytest && \
    mkdir -p /home/user && \
    chmod 755 /home/user && \
    if ! id -u user >/dev/null 2>&1; then \
        useradd -m -d /home/user -s /bin/bash user; \
    fi && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Environment section
ENV PATH="/usr/local/bin:/usr/bin:/bin:$PATH"

# Default action when the container is executed
CMD ["/bin/bash"]