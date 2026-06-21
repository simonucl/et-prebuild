FROM ubuntu:22.04

RUN set -e && \
    apt-get update && \
    apt-get install -y --no-install-recommends python3 python3-pip && \
    pip3 install --no-cache-dir pytest && \
    mkdir -p /home/user/staging_rules && \
    mkdir -p /home/user/monitoring/rules/enabled

RUN cat > /home/user/staging_rules/critical_load.rule <<'EOF'
alert: cpu_load
severity: critical
threshold: 0.85
EOF

RUN chmod 755 /home/user && \
    chmod 755 /home/user/monitoring && \
    chmod 755 /home/user/monitoring/rules && \
    chmod 777 /home/user/monitoring/rules/enabled && \
    chmod 755 /home/user/staging_rules && \
    chmod 644 /home/user/staging_rules/critical_load.rule

ENV HOME=/home/user