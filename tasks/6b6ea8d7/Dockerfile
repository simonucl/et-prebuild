# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# %post section
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip set -e && \
    apt-get update && \
    apt-get install -y --no-install-recommends python3 python3-pip && \
    pip3 install --no-cache-dir pytest && \
    mkdir -p /home/user/data

RUN cat >/home/user/data/raw_run1.csv <<'EOF'
timestamp,endpoint,latency_ms
2023-09-01T10:00:00Z,/api/login,120
2023-09-01T10:00:01Z,/api/items,200
2023-09-01T10:00:02Z,/api/login,110
2023-09-01T10:00:03Z,/api/items,220
2023-09-01T10:00:04Z,/api/items,180
EOF

RUN cat >/home/user/data/raw_run2.csv <<'EOF'
timestamp,endpoint,latency_ms
2023-09-01T11:00:00Z,/api/login,130
2023-09-01T11:00:01Z,/api/items,210
2023-09-01T11:00:02Z,/api/login,140
2023-09-01T11:00:03Z,/api/items,190
2023-09-01T11:00:04Z,/api/login,150
EOF

RUN chmod 0755 /home/user && \
    chmod 0755 /home/user/data && \
    chmod 0644 /home/user/data/raw_run1.csv /home/user/data/raw_run2.csv

# %environment section
ENV LANG=C.UTF-8 \
    LC_ALL=C.UTF-8