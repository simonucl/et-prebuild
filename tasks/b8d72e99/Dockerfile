# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# Help / labels
LABEL Author="dev-helper"
LABEL Description="Environment for the 'sample_app' diagnostic task with pytest pre-installed."

# Install required packages
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip set -e && \
    apt-get update -y && \
    apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        jq \
        ca-certificates \
        dumb-init && \
    pip3 install --no-cache-dir pytest

# Create non-root user (UID/GID 1000)
RUN groupadd -g 1000 user || true && \
    useradd -m -u 1000 -g 1000 user || true

# Prepare directories
RUN mkdir -p /home/user/sample_app/logs

# status.json
RUN cat <<'EOF' > /home/user/sample_app/status.json
{"pid": 4242, "cpu_pct": 2.3, "mem_pct": 1.1, "open_ports": [8080, 9090]}
EOF
RUN chmod 0600 /home/user/sample_app/status.json

# app.log
RUN cat <<'EOF' > /home/user/sample_app/logs/app.log
[2023-07-10 10:00:00] INFO  Starting service
[2023-07-10 10:01:00] INFO  Initialising configuration
[2023-07-10 10:02:13] ERROR Connection timed out to database
[2023-07-10 10:02:14] WARN  Retrying connection
[2023-07-10 10:02:20] ERROR Connection timed out to database
[2023-07-10 10:05:33] INFO  Configuration reloaded
[2023-07-10 10:10:04] ERROR Failed to load configuration file
[2023-07-10 10:15:42] INFO  Health-check passed
[2023-07-10 10:20:11] ERROR User authentication failed
[2023-07-10 10:25:00] INFO  Shutting down
EOF
RUN chmod 0644 /home/user/sample_app/logs/app.log

# Adjust ownership and permissions
RUN chown -R 1000:1000 /home/user && \
    chmod 755 /home/user

# Environment variables
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

USER 1000
WORKDIR /home/user