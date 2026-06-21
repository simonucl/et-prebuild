# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# From %post
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest && \
    mkdir -p /home/user && \
    chmod 0777 /home/user

# From %environment — create a startup script
RUN cat <<'EOF' > /usr/local/bin/container_env.sh
#!/bin/sh
chmod 755 /home/user

if [ ! -d /home/user ]; then
    mkdir -p /home/user
    chmod 0777 /home/user
fi

if [ ! -d /home/user/logs ]; then
    mkdir -p /home/user/logs
    chmod 0755 /home/user/logs
fi

if [ ! -f /home/user/logs/system.log ]; then
    cat > /home/user/logs/system.log <<'LOGEOF'
2023-07-01 12:00:01 FAILED LOGIN user=root
2023-07-01 12:01:15 ERROR Disk quota exceeded
2023-07-01 12:02:45 WARNING High memory usage detected
2023-07-01 12:03:00 FAILED LOGIN user=admin
2023-07-01 12:03:30 ERROR Cannot open configuration file
2023-07-01 12:04:05 WARNING CPU temperature high
2023-07-01 12:05:20 ERROR Invalid user input
2023-07-01 12:06:10 FAILED LOGIN user=test
2023-07-01 12:07:55 ERROR Service unavailable
2023-07-01 12:08:30 ERROR Timeout while connecting to DB
LOGEOF
    chmod 0644 /home/user/logs/system.log
fi

export LC_ALL=C.UTF-8
export LANG=C.UTF-8

exec "$@"
EOF

RUN chmod +x /usr/local/bin/container_env.sh

# From %labels
LABEL Author="Security-Log Task Setup"
LABEL Description="Base image providing initial state and pytest for automated grading."

ENTRYPOINT ["/usr/local/bin/container_env.sh"]