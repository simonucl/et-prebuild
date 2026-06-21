# syntax=docker/dockerfile:1
FROM ubuntu:22.04

RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip set -e && \
    apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        ca-certificates && \
    pip3 install --no-cache-dir pytest && \
    mkdir -p /home/user && \
    mkdir -p /home/user/releases/shared/config && \
    mkdir -p /home/user/releases/shared/scripts && \
    mkdir -p /home/user/releases/release-1.0.0 && \
    mkdir -p /home/user/logs && \
    mkdir -p /home/user/uploads && \
    mkdir -p /home/user/deployment_logs && \
    printf 'staging: {}\n' > /home/user/releases/shared/config/settings.yml

RUN cat << 'EOF' > /home/user/releases/shared/scripts/start.sh
#!/bin/bash
echo starting
EOF

RUN cat << 'EOF' > /home/user/releases/shared/scripts/stop.sh
#!/bin/bash
echo stopping
EOF

RUN chmod 755 /home/user/releases/shared/scripts/start.sh && \
    chmod 755 /home/user/releases/shared/scripts/stop.sh && \
    ln -s /home/user/releases/release-1.0.0 /home/user/current && \
    chmod -R a+rX /home/user && \
    chmod -R a+rwX /home/user/logs /home/user/uploads /home/user/deployment_logs

ENV PATH="/usr/bin:$PATH"

CMD ["sh", "-c", "echo \"Container for Release-Manager task. Execute your automation script inside.\""]