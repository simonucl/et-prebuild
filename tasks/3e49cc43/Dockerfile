FROM ubuntu:22.04

# Author Observability Exercise Setup
# Description Base image with initial filesystem state for Grafana dashboard linking task.

RUN set -e && \
    echo "Updating package index and installing prerequisites..." && \
    apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3-pip \
        ca-certificates \
        build-essential && \
    echo "Installing pytest for the runtime environment..." && \
    pip3 install --no-cache-dir pytest

RUN mkdir -p /home/user/observability/dashboards/available && \
    mkdir -p /home/user/observability/dashboards/enabled

RUN cat > /home/user/observability/dashboards/available/net_traffic.json <<'EOF'
{
    "title": "Network Traffic",
    "panels": [
        {
            "id": 1,
            "type": "graph",
            "title": "Inbound",
            "targets": [
                { "expr": "sum(rate(node_network_receive_bytes_total[5m]))" }
            ]
        },
        {
            "id": 2,
            "type": "graph",
            "title": "Outbound",
            "targets": [
                { "expr": "sum(rate(node_network_transmit_bytes_total[5m]))" }
            ]
        }
    ]
}
EOF

RUN cat > /home/user/observability/dashboards/available/cpu_load.json <<'EOF'
{
    "title": "CPU Load",
    "panels": [
        {
            "id": 1,
            "type": "graph",
            "title": "Load Average",
            "targets": [
                { "expr": "node_load1" }
            ]
        }
    ]
}
EOF

RUN echo "Setting liberal permissions so the unprivileged agent can modify contents..." && \
    chmod -R 777 /home/user/observability && \
    chmod 755 /home/user && \
    echo "Cleaning up APT cache..." && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*