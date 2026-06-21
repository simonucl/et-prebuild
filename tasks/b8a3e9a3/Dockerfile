# syntax=docker/dockerfile:1
# Author: Apptainer Task Setup
# Description: Environment for converting users.json to users.csv
# This container provides the starting point for the JSON → CSV conversion task.
# The dataset is located at /home/user/project/assets/users.json
# Write your CSV to /home/user/project/exports/users.csv
# pytest is installed for test execution.

FROM ubuntu:22.04

RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip set -e && \
    apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3-pip \
        jq \
        ca-certificates && \
    pip3 install --no-cache-dir pytest

RUN set -e && \
    mkdir -p /home/user/project/assets && \
    mkdir -p /home/user/project/exports

RUN cat > /home/user/project/assets/users.json <<'EOF'
[
  {"id":1,"name":"Ada Lovelace","email":"ada@example.com"},
  {"id":2,"name":"Linus Torvalds","email":"linus@example.com"},
  {"id":3,"name":"Grace Hopper","email":"grace@example.com"}
]
EOF

RUN chmod -R a+rX /home/user && \
    chmod -R a+w /home/user/project/exports

RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked apt-get clean && rm -rf /var/lib/apt/lists/*

ENV PATH=/usr/local/bin:/usr/bin:/bin:$PATH