# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# Install Python and pytest
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip set -eux && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        ca-certificates && \
    pip3 install --no-cache-dir pytest

# Create required directory structure and baseline log file
RUN set -eux && \
    mkdir -p /home/user/app/logs

RUN cat >/home/user/app/logs/app.log <<'EOF'
2023-08-10 12:00:01 INFO 100 RequestID=abc123 User=alice IP=192.168.1.10 Successful login
2023-08-10 12:05:47 ERROR 500 RequestID=def456 User=bob IP=10.0.0.42 NullPointerException at line 42
2023-08-10 12:07:33 WARN 300 RequestID=ghi789 User=carol IP=172.16.5.3 Slow response
2023-08-10 12:12:11 ERROR 404 RequestID=jkl012 User=dave IP=192.168.1.55 Resource not found /favicon.ico
2023-08-10 12:15:27 ERROR 500 RequestID=mno345 User=erin IP=10.0.0.99 NullPointerException at line 87
2023-08-10 12:15:28 INFO 100 RequestID=pqr678 User=frank IP=172.16.5.3 Logout
2023-08-10 12:18:00 ERROR 403 RequestID=stu901 User=gina IP=192.168.1.10 Forbidden access to /admin
2023-08-10 12:19:15 ERROR 404 RequestID=vwx234 User=henry IP=192.168.1.55 Resource not found /robots.txt
EOF

# Ensure non-root users inside the container can write the artefacts
RUN set -eux && \
    chmod -R a+rwX /home/user/app/logs && \
    chmod -R a+rX /home/user/app && \
    chmod 755 /home/user

# Clean up APT to make the image smaller
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked set -eux && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

LABEL Author="devops-task-prep" \
      Description="Initial state for log-processing task: only app.log exists; pytest pre-installed."