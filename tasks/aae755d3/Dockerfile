# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# Author: Apptainer Task Setup
# Description: Environment prepared for IoT deployment error count task with pytest installed.
# Help:
#   This container image provides the initial state for the IoT deployment
#   log counting task. It includes:
#     - /home/user/device_deploy.log with predefined contents
#     - pytest pre-installed for automated testing

RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked set -e && \
    apt-get update && \
    apt-get install -y --no-install-recommends python3 python3-pip && \
    rm -rf /var/lib/apt/lists/*

RUN --mount=type=cache,target=/root/.cache/pip pip3 install --no-cache-dir pytest

RUN mkdir -p /home/user

RUN cat > /home/user/device_deploy.log <<'EOF'
2023-10-01 10:00:00 [INFO]  Deployment started
2023-10-01 10:01:00 [ERROR] Connection timeout
2023-10-01 10:02:00 [INFO]  Retrying deployment
2023-10-01 10:03:00 [ERROR] Authentication failed
2023-10-01 10:04:00 [INFO]  Deployment aborted
2023-10-01 10:05:00 [ERROR] Rollback failed
2023-10-01 10:06:00 [INFO]  Support notified
EOF

RUN chmod 0755 /home/user && \
    chmod 0644 /home/user/device_deploy.log

# Equivalent of %runscript:
# chmod 755 /home/user
# exec "$@"

CMD ["/bin/bash"]