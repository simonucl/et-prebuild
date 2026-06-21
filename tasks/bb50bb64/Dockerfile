# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# Help section
# Container built for the 'alert stream' exercise.

RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip set -e && \
    apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        python3-setuptools \
        ca-certificates && \
    pip3 install --no-cache-dir --upgrade pip && \
    pip3 install --no-cache-dir pytest && \
    mkdir -p /home/user/data

RUN cat > /home/user/data/event_feed.csv <<'EOF'
event_id,timestamp,service,severity,message
1001,2024-01-14T09:15:22Z,auth,INFO,User login successful
1002,2024-01-14T09:18:05Z,database,CRITICAL,Database connection lost
1003,2024-01-14T09:20:47Z,web,WARN,High latency detected
1004,2024-01-14T09:22:10Z,filesystem,CRITICAL,Disk space critically low
1005,2024-01-14T09:25:33Z,auth,INFO,User logout
1006,2024-01-14T09:30:01Z,network,MAJOR,Packet loss above threshold
1007,2024-01-14T09:35:17Z,security,CRITICAL,Multiple failed logins
1008,2024-01-14T09:40:00Z,backup,INFO,Backup completed
EOF

RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked chmod 644 /home/user/data/event_feed.csv && \
    chmod 777 /home/user && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

RUN chmod 755 /home/user