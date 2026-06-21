# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# Maintainer backup-task-setup

RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip set -e && \
    apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest

RUN mkdir -p /home/user && \
    chmod 0777 /home/user && \
    mkdir -p /home/user/project/config

RUN cat <<'EOF' > /home/user/project/config/app.conf
[app]
version=1.2.3
name=ExampleApp
EOF

RUN cat <<'EOF' > /home/user/project/config/db.conf
[database]
host=localhost
port=5432
user=admin
pass=secret
EOF

RUN cat <<'EOF' > /home/user/project/config/net.conf
[network]
interface=eth0
address=192.168.1.100
EOF

RUN chmod -R a+rX /home/user && chmod 755 /home/user

CMD ["bash"]