# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# Author: Capacity-Planning Exercise
# Description: Base image providing the raw input data and test framework

ENV PYTHONUNBUFFERED=1

RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked set -e && \
    export DEBIAN_FRONTEND=noninteractive && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        ca-certificates && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN --mount=type=cache,target=/root/.cache/pip pip3 install --no-cache-dir pytest

RUN set -e && \
    if ! id -u user >/dev/null 2>&1; then \
        useradd -m -u 1000 -s /bin/bash user || useradd -m -s /bin/bash user; \
    fi

RUN mkdir -p /home/user/capacity/raw

RUN cat <<'EOF' > /home/user/capacity/raw/serverA.csv
timestamp,cpu_pct,mem_mb
2023-07-01T00:00:00,55.5,2048
2023-07-01T01:00:00,65.0,2100
2023-07-01T02:00:00,70.2,2200
2023-07-01T03:00:00,60.1,2000
EOF

RUN cat <<'EOF' > /home/user/capacity/raw/serverB.csv
timestamp,cpu_pct,mem_mb
2023-07-01T00:00:00,35.2,1024
2023-07-01T01:00:00,45.5,1100
2023-07-01T02:00:00,50.0,1150
2023-07-01T03:00:00,40.3,1080
EOF

RUN chmod -R a+rX /home/user/capacity && \
    chmod a+rwx /home/user/capacity && \
    rm -rf /home/user/capacity/analysis || true && \
    rm -rf /home/user/capacity/logs || true && \
    chmod 755 /home/user

CMD echo "Capacity-planning base container. No default command defined." && \
    echo "Launch your own scripts inside this container as needed."