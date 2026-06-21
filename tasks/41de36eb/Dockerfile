FROM ubuntu:22.04

# Author "Container Prepared for Monitoring Ticket Exercise"

RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        curl \
        ca-certificates && \
    pip3 install --no-cache-dir pytest

RUN mkdir -p /home/user/mock_api/auth && \
    mkdir -p /home/user/mock_api/files && \
    mkdir -p /home/user/mock_api/billing && \
    mkdir -p /home/user/ticket_logs

RUN cat <<'EOF' > /home/user/mock_api/auth/status.json
{ "service": "auth", "status": "ok" }
EOF

RUN cat <<'EOF' > /home/user/mock_api/files/status.json
{ "service": "files", "status": "ok" }
EOF

RUN cat <<'EOF' > /home/user/mock_api/billing/status.json
{ "service": "billing", "status": "degraded" }
EOF

RUN chmod -R 0755 /home/user && \
    chmod 0777 /home/user/ticket_logs

RUN chmod 755 /home/user

ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

LABEL Author="Container Prepared for Monitoring Ticket Exercise"