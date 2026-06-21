# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# ------------------------------------------------------------------
# Install Python tooling and pytest
# ------------------------------------------------------------------
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# ------------------------------------------------------------------
# Create initial filesystem layout for the exercise
# ------------------------------------------------------------------
RUN set -e && \
    mkdir -p /home/user && \
    chmod 755 /home/user && \
    \
    mkdir -p /home/user/projects && \
    chmod 755 /home/user/projects && \
    \
    mkdir -p /home/user/projects/app_alpha/bin && \
    mkdir -p /home/user/projects/app_alpha/log && \
    \
    dd if=/dev/zero of=/home/user/projects/app_alpha/bin/dummy.bin bs=1M count=1 status=none && \
    dd if=/dev/zero of=/home/user/projects/app_alpha/log/logfile.log bs=1M count=3 status=none && \
    dd if=/dev/zero of=/home/user/projects/app_alpha/README.md bs=4K count=1 status=none && \
    \
    mkdir -p /home/user/projects/app_beta/data && \
    mkdir -p /home/user/projects/app_beta/docs && \
    \
    dd if=/dev/zero of=/home/user/projects/app_beta/data/data.bin bs=1M count=1 status=none && \
    dd if=/dev/zero of=/home/user/projects/app_beta/docs/doc.bin bs=1M count=1 status=none && \
    \
    mkdir -p /home/user/projects/app_gamma/src && \
    mkdir -p /home/user/projects/app_gamma/tests && \
    \
    dd if=/dev/zero of=/home/user/projects/app_gamma/src/src.bin bs=1M count=4 status=none && \
    dd if=/dev/zero of=/home/user/projects/app_gamma/tests/test.bin bs=1M count=1 status=none && \
    dd if=/dev/zero of=/home/user/projects/app_gamma/report.pdf bs=1M count=1 status=none && \
    \
    find /home/user -type d -exec chmod 755 {} + && \
    find /home/user -type f -exec chmod 644 {} +

# ------------------------------------------------------------------
# Environment variables
# ------------------------------------------------------------------
ENV LC_ALL=C