FROM ubuntu:22.04

# Author ChatGPT
# Description Environment for diagnostic rsync task – provides initial source files and pytest.

RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3-pip \
        rsync \
        ca-certificates && \
    pip3 install --no-cache-dir pytest && \
    mkdir -p /home/user && \
    chmod 0777 /home/user && \
    SRC_DIR="/home/user/support_source" && \
    mkdir -p "${SRC_DIR}"

RUN cat <<'EOF' > /home/user/support_source/config.conf
max_connections=200
log_level=debug
EOF

RUN cat <<'EOF' > /home/user/support_source/status.json
{
  "service": "web-api",
  "status": "running",
  "uptime": 43200
}
EOF

RUN cat <<'EOF' > /home/user/support_source/system.log
2024-01-01 00:00:01 INFO System boot
2024-01-01 00:00:05 INFO Diagnostics initialized
2024-01-01 00:10:12 WARN High memory usage detected
EOF

RUN chmod -R a+r /home/user/support_source && \
    chmod a+rx /home/user/support_source && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN chmod 755 /home/user

ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

CMD echo "This container sets up the environment for the diagnostic rsync task." && \
    echo "Use \`docker run\` with your own commands or run tests with pytest."