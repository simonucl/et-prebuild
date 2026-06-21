# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# Help / labels from %help and %labels
LABEL Author="Apptainer Task Setup"
LABEL Description="Environment for log filtering task with pytest pre-installed"

# 1. Install Python and pytest
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip set -e && \
    export DEBIAN_FRONTEND=noninteractive && \
    apt-get update -qq && \
    apt-get install -y --no-install-recommends python3 python3-pip && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# 2. Filesystem setup
RUN mkdir -p /home/user/logs && \
    chmod 0777 /home/user/logs

RUN cat <<'EOF' > /home/user/logs/app.log
2023-08-15 13:45:12,123 INFO  Request from 10.0.0.1 processed in 120ms
2023-08-15 14:00:03,001 ERROR Database connection failed for user app
2023-08-15 14:12:55,789 WARN  Cache miss for key user_42
2023-08-15 14:22:11,456 ERROR Timeout while calling external API
2023-08-15 14:45:00,999 FATAL Unhandled exception in payment service
2023-08-15 15:00:00,000 INFO  Scheduled job started
2023-08-14 14:30:32,222 ERROR Previous day error.
EOF

RUN chmod 0644 /home/user/logs/app.log

# Environment variables from %environment
RUN chmod 755 /home/user
ENV PATH=/usr/local/bin:/usr/bin:/bin:$PATH

# Runscript equivalent
CMD echo "This container provides the initial state for the log filtering task." && \
    echo "Please execute your solution commands inside an interactive shell:" && \
    echo "    docker run -it <image> /bin/bash"