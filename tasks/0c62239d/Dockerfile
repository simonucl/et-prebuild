# Container providing the initial state for the CI/CD cut-over exercise.
# Includes pytest for the test harness.
# Author: CI Task Generator

FROM ubuntu:22.04

ENV HOME=/home/user

RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    rm -rf /var/lib/apt/lists/*

RUN pip3 install --no-cache-dir pytest

RUN mkdir -p /home/user/repos/ci-cd-scripts/releases/v0.9

RUN cat <<'EOF' > /home/user/repos/ci-cd-scripts/releases/v0.9/deploy.sh
#!/usr/bin/env bash
echo "Deploy v0.9"
EOF

RUN chmod +x /home/user/repos/ci-cd-scripts/releases/v0.9/deploy.sh

RUN ln -sfn releases/v0.9 /home/user/repos/ci-cd-scripts/current

RUN chmod -R a+rX /home/user