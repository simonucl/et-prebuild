# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# Author: Apptainer Task Setup
# Description: Environment prepared for API-level connectivity task with pytest pre-installed.

RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked set -e && \
    apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3-pip \
        ca-certificates \
        curl && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN --mount=type=cache,target=/root/.cache/pip pip3 install --no-cache-dir pytest

RUN mkdir -p /home/user/mock_api && \
    chmod 755 /home/user && \
    chmod 755 /home/user/mock_api

RUN cat > /home/user/mock_api/ok.json <<'EOF'
{"status":"ok"}
EOF

RUN chmod 644 /home/user/mock_api/ok.json

ENV PATH=/usr/local/bin:/usr/bin:/bin:$PATH

CMD echo "Container ready. Drop into a shell or execute your task commands." && exec /bin/bash "$@"