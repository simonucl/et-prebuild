FROM ubuntu:22.04

# Basic tooling
RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Python testing framework
RUN pip3 install --no-cache-dir pytest

# Seed initial filesystem state
RUN mkdir -p /home/user/observability/raw_metrics

RUN cat > /home/user/observability/raw_metrics/cpu_metrics.csv <<'EOF'
timestamp,cpu_usage_percent
2024-06-01T10:00:00Z,45.3
2024-06-01T11:00:00Z,55.1
2024-06-01T12:00:00Z,49.8
EOF

RUN cat > /home/user/observability/raw_metrics/memory_metrics.csv <<'EOF'
timestamp,mem_used_mb
2024-06-01T10:00:00Z,7832
2024-06-01T11:00:00Z,8124
2024-06-01T12:00:00Z,7998
EOF

RUN cat > /home/user/observability/raw_metrics/http_requests.csv <<'EOF'
timestamp,method,status_code,latency_ms
2024-06-01T10:00:00Z,GET,200,123
2024-06-01T10:01:00Z,POST,200,256
2024-06-01T10:02:00Z,GET,500,789
2024-06-01T11:15:00Z,GET,200,101
2024-06-01T12:22:00Z,POST,404,303
EOF

RUN chmod -R a+rX /home/user

ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8
ENV HOME=/home/user

RUN chmod 755 /home/user