FROM ubuntu:22.04

# Help section (from original Apptainer file)
# Installs Python, pytest, and prepares initial filesystem state

ENV PYTHONDONTWRITEBYTECODE=1
ENV LANG=C.UTF-8
ENV LC_ALL=C.UTF-8

RUN set -e && \
    export DEBIAN_FRONTEND=noninteractive && \
    apt-get update && \
    apt-get install -y --no-install-recommends python3 python3-pip && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN mkdir -p /home/user/helpdesk/logs && \
    chmod 755 /home/user/helpdesk/logs

RUN cat > /home/user/helpdesk/logs/2023-Sept-Audit.log << 'EOF'
2023-09-01 00:00:01 Start of audit
2023-09-01 00:05:47 Audit completed
EOF

RUN chmod 644 /home/user/helpdesk/logs/2023-Sept-Audit.log