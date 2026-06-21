FROM ubuntu:22.04

# Help section from Apptainer definition
# This container sets up network exercise environment with logs and reports.

RUN set -e && \
    apt-get update -y && \
    apt-get install -y --no-install-recommends \
        python3-pip \
        jq \
        ca-certificates && \
    pip3 install --no-cache-dir pytest && \
    mkdir -p /home/user && \
    chmod 755 /home/user && \
    BASE_DIR="/home/user/network" && \
    LOG_DIR="${BASE_DIR}/logs" && \
    REPORTS_DIR="${BASE_DIR}/reports" && \
    mkdir -p "${LOG_DIR}" "${REPORTS_DIR}" && \
    chmod 0777 "${REPORTS_DIR}"

RUN cat > /home/user/network/logs/ping_results.csv <<'EOF'
timestamp,host,latency_ms,packet_loss
2023-07-01T10:00:00Z,host1.example.com,23,0
2023-07-01T10:00:00Z,host2.example.com,,100
2023-07-01T10:00:00Z,host3.example.com,45,0
2023-07-01T10:00:00Z,host4.example.com,,100
2023-07-01T10:00:00Z,host5.example.com,31,0
EOF

RUN chmod 0644 /home/user/network/logs/ping_results.csv && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

ENV PATH="/usr/local/bin:/usr/bin:/bin:${PATH}"