FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

# Help/label metadata
LABEL Author="compliance-task-image"

RUN set -e && \
    apt-get update && \
    apt-get install -y --no-install-recommends python3-pip && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

RUN pip3 install --no-cache-dir pytest

RUN mkdir -p /home/user && \
    mkdir -p /home/user/audit/reports

RUN cat > /home/user/audit/reports/annual_2024.txt <<'EOF'
Compliance Report 2024
All systems passed baseline checks.
EOF

RUN chmod 0777 /home/user/audit && \
    chmod 0777 /home/user/audit/reports && \
    chmod 0666 /home/user/audit/reports/annual_2024.txt && \
    chmod 755 /home/user