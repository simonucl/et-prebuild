FROM ubuntu:22.04

# Author: AI Assistant
# Description: Container for uptime-monitoring exercise with pytest installed.

RUN set -e && \
    apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3-pip \
        ca-certificates && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN set -e && \
    MON_DIR="/home/user/monitoring" && \
    mkdir -p "${MON_DIR}" && \
    chmod 0777 "${MON_DIR}"

RUN MON_DIR="/home/user/monitoring" && \
    cat > "${MON_DIR}/monitors.ini" <<'EOF'
[web]
url = https://example.com
expected_status = 200

[db]
url = tcp://db.internal:5432
expected_status = alive

[cache]
url = tcp://cache.internal:6379
expected_status = alive
EOF

RUN chmod 0644 /home/user/monitoring/monitors.ini

RUN chmod 755 /home/user

ENV LC_ALL=C.UTF-8
ENV PYTHONIOENCODING=UTF-8

LABEL Author="AI Assistant"
LABEL Description="Container for uptime-monitoring exercise with pytest installed."