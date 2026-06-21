# syntax=docker/dockerfile:1
# Converted from Apptainer definition
FROM ubuntu:22.04

# Help / labels
# Author: devsecops-task-prep
# Description: Container for access-control policy coding exercise: provides log fixture and pytest.
LABEL Author="devsecops-task-prep" \
      Description="Container for access-control policy coding exercise: provides log fixture and pytest."

# Environment variables
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

# Ensure /home/user exists with correct permissions
RUN mkdir -p /home/user && chmod 755 /home/user

RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked set -e && \
    echo "Updating package index and installing required packages ..." && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        ca-certificates \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

RUN --mount=type=cache,target=/root/.cache/pip pip3 install --no-cache-dir pytest

RUN mkdir -p /home/user/simulated_logs && chmod -R 0777 /home/user

RUN cat > /home/user/simulated_logs/auth-service.log <<'LOGEOF'
[2023-09-01 12:00:00] INFO  User login succeeded: user=jdoe   ip=192.168.0.10
[2023-09-01 12:01:00] WARN  User login failed:    user=jdoe   ip=192.168.0.10
[2023-09-01 12:02:00] WARN  User login failed:    user=jdoe   ip=192.168.0.10
[2023-09-01 12:03:00] WARN  User login failed:    user=alice  ip=10.0.0.5
[2023-09-01 12:04:00] INFO  User login succeeded: user=alice  ip=10.0.0.5
[2023-09-01 12:05:00] WARN  User login failed:    user=bob    ip=172.16.1.3
[2023-09-01 12:06:00] WARN  User login failed:    user=bob    ip=172.16.1.3
[2023-09-01 12:07:00] WARN  User login failed:    user=bob    ip=172.16.1.3
[2023-09-01 12:08:00] DEBUG Heartbeat check ok
[2023-09-01 12:09:00] WARN  User login failed:    user=charlie ip=192.168.0.20
LOGEOF

RUN chmod 0644 /home/user/simulated_logs/auth-service.log