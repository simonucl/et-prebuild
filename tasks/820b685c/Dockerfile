# Maintainer: container-builder
# Description: Environment for INI summary exercise with pytest pre-installed.

FROM ubuntu:22.04

ENV PATH="/usr/local/bin:/usr/bin:/bin:$PATH"

RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN mkdir -p /home/user/project

RUN cat > /home/user/project/perf_settings.ini <<'EOF'
[database]
max_connections = 200
timeout_seconds = 60

[server]
thread_pool_size = 32
enable_caching = true

[logging]
level = INFO
rotate = daily
EOF

RUN chmod 0644 /home/user/project/perf_settings.ini && \
    chmod 0755 /home && \
    chmod 0755 /home/user && \
    chmod 0755 /home/user/project