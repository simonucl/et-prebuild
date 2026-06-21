# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# Author: benchmark-setup
# Description: Container pre-configured with a one-off performance log for automated testing.

RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip set -eux && \
    export DEBIAN_FRONTEND=noninteractive && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
        sysbench \
        python3-pip && \
    pip3 install --no-cache-dir pytest && \
    useradd -m -d /home/user -s /bin/bash user && \
    mkdir -p /home/user/benchmarks && \
    chown -R user:user /home/user

RUN set -eux && \
    cat <<EOF > /home/user/benchmarks/performance.log
DISK_WRITE_MB_S: 500.0
CPU_EVENTS_PER_SEC: 10000.0
TIMESTAMP: $(date '+%Y-%m-%d %H:%M:%S')
EOF

RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked set -eux && \
    chmod 0755 /home/user && \
    chmod 0755 /home/user/benchmarks && \
    chmod 0644 /home/user/benchmarks/performance.log && \
    chown -R user:user /home/user && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

ENV PATH=/usr/local/bin:/usr/bin:/bin:$PATH

USER user
WORKDIR /home/user