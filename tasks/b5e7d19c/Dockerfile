# syntax=docker/dockerfile:1
# Converted from Apptainer definition file
FROM ubuntu:22.04

# Basic tooling: Python and PyPI, then install pytest
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest

# Prepare initial filesystem state required by the exercise
RUN mkdir -p /home/user/deployments && \
    chmod 755 /home/user/deployments

RUN cat > /home/user/deployments/updates-2023-06-30.log <<'EOF'
2023-06-30T10:00:00Z node_id=node-a STATUS=SUCCESS version=2.1.0
2023-06-30T10:00:02Z node_id=node-b STATUS=FAIL    version=2.1.0
2023-06-30T10:00:04Z node_id=node-c STATUS=SUCCESS version=2.1.0
2023-06-30T10:00:06Z node_id=node-d STATUS=SUCCESS version=2.1.0
2023-06-30T10:00:08Z node_id=node-e STATUS=FAIL    version=2.1.0
2023-06-30T10:00:10Z node_id=node-f STATUS=SUCCESS version=2.1.0
2023-06-30T10:00:12Z node_id=node-g STATUS=SUCCESS version=2.1.0
EOF

RUN chmod 644 /home/user/deployments/updates-2023-06-30.log

# Clean apt caches
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked apt-get clean && rm -rf /var/lib/apt/lists/*

# Environment variables
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8