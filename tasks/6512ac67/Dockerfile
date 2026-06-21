# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# Labels from Apptainer definition
LABEL Author="Capacity-Planning Task Builder"
LABEL Description="Base image for capacity-planning exercise with initial log data and pytest installed."

# --------------------------------------------------------------------- #
# Install system packages and pytest
# --------------------------------------------------------------------- #
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked set -e && \
    export DEBIAN_FRONTEND=noninteractive && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
        python3-pip \
        bc \
        ca-certificates && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN --mount=type=cache,target=/root/.cache/pip pip3 install --no-cache-dir pytest

# --------------------------------------------------------------------- #
# Create non-root user and prepare filesystem state
# --------------------------------------------------------------------- #
RUN useradd -m -d /home/user -s /bin/bash user

# Create logs directory and populate the log file
RUN mkdir -p /home/user/logs

RUN cat <<'EOF' > /home/user/logs/container_stats_2023-09-15.log
container_id,name,cpu_percent,mem_usage_mb
1db3aa112,web_frontend,35.5,512
2ab4cc223,database,82.7,1500
3cd5dd334,cache,18.2,256
4de6ee445,worker,77.9,1100
5ef7ff556,nginx_proxy,23.0,450
6fa8gg667,analytics,69.4,2048
EOF

# Ensure appropriate permissions so the non-root runtime user can read
RUN chmod 644 /home/user/logs/container_stats_2023-09-15.log && \
    chmod 755 /home/user /home/user/logs && \
    chown -R user:user /home/user

# --------------------------------------------------------------------- #
# Environment (no special variables required)
# --------------------------------------------------------------------- #
ENV HOME=/home/user

# Use non-root user by default
USER user
WORKDIR /home/user

# --------------------------------------------------------------------- #
# Help
# Base image for capacity-planning exercise with initial log data and pytest installed.
# --------------------------------------------------------------------- #