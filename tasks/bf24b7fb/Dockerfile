# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# %post
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip set -e && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        procps && \
    pip3 install --no-cache-dir pytest

RUN mkdir -p /home/user/deployment && \
    chmod 0777 /home/user /home/user/deployment

RUN cat <<'EOF' >/home/user/deployment/deploy_app.sh
#!/bin/bash
while true; do
    echo "Deploying..." >> /home/user/deployment/app.log
    sleep 60
done
EOF

RUN chmod 755 /home/user/deployment/deploy_app.sh

# %environment
ENV PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin