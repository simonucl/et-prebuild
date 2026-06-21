# syntax=docker/dockerfile:1
FROM ubuntu:22.04

RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3-pip tar ca-certificates && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

RUN --mount=type=cache,target=/root/.cache/pip pip3 install --no-cache-dir pytest

RUN mkdir -p /home/user/monitoring

RUN cat <<'EOF' > /home/user/monitoring/service1-uptime-2023-09.csv
date,uptime_percentage
2023-09-01,99.98
2023-09-02,99.99
2023-09-03,99.97
EOF

RUN cat <<'EOF' > /home/user/monitoring/service2-uptime-2023-09.csv
date,uptime_percentage
2023-09-01,99.95
2023-09-02,99.96
2023-09-03,99.94
EOF

RUN chmod 755 /home/user && \
    chmod 755 /home/user/monitoring && \
    chmod 644 /home/user/monitoring/service*-uptime-2023-09.csv

ENV PATH="/usr/local/bin:/usr/bin:${PATH}"

# Help: Initial filesystem setup with monitoring CSV files