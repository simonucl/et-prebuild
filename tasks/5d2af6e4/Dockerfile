# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# ------------------------------------------------------------------
# Install Python, pip, and pytest
# ------------------------------------------------------------------
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip set -e && \
    apt-get update && \
    apt-get install -y --no-install-recommends python3 python3-pip && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# ------------------------------------------------------------------
# Create a non-privileged user `user` (UID 1000 / GID 1000)
# ------------------------------------------------------------------
RUN set -e && \
    if ! getent group 1000 >/dev/null; then \
        groupadd -g 1000 user; \
    fi && \
    if ! id -u 1000 >/dev/null 2>&1; then \
        useradd -m -u 1000 -g 1000 -s /bin/bash user; \
    fi

# ------------------------------------------------------------------
# Prepare initial filesystem state expected by the tests
# ------------------------------------------------------------------
RUN set -e && \
    chown 1000:1000 /home/user && \
    chmod 755 /home/user && \
    mkdir -p /home/user/new-certs && \
    chown 1000:1000 /home/user/new-certs && \
    chmod 755 /home/user/new-certs

# Create the initial certificate file (exactly 3 bytes: "abc")
RUN set -e && \
    printf 'abc' > /home/user/new-certs/internal.pem && \
    chown 1000:1000 /home/user/new-certs/internal.pem && \
    chmod 644 /home/user/new-certs/internal.pem

# ------------------------------------------------------------------
# Environment variables
# ------------------------------------------------------------------
ENV PATH=/usr/local/bin:/usr/bin:/bin:$PATH

# ------------------------------------------------------------------
# Help / runscript information
# ------------------------------------------------------------------
# Container for certificate-management task.
# Switch to the non-privileged user with:  su - user
# Then perform the required operations.