# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# %post
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip set -e && \
    echo "Updating apt repositories and installing python + pip..." && \
    apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        ca-certificates && \
    pip3 install --no-cache-dir pytest && \
    rm -rf /var/lib/apt/lists/*

RUN set -e && \
    echo "Creating initial directory structure and fixture log file..." && \
    mkdir -p /home/user/logs && \
    chmod 777 /home/user

RUN cat > /home/user/logs/app.log <<'EOF'
2024-06-01 10:12:33 INFO User login succeeded
2024-06-01 10:15:41 ERROR 404 Page not found
2024-06-01 10:17:02 WARNING Disk space low
2024-06-01 10:20:11 CRITICAL Database connection lost
2024-06-01 10:25:59 ERROR 500 Internal server error
2024-06-01 10:30:12 INFO Scheduled backup completed
2024-06-01 10:35:44 ERROR 502 Bad gateway
2024-06-01 10:40:23 DEBUG Cache cleared
EOF

RUN chmod 644 /home/user/logs/app.log

# %environment
RUN chmod 755 /home/user

# %runscript
# Container for the 'log-monitoring' exercise.
# Use an interactive shell:
#   docker run -it <image> /bin/bash
# to begin working.