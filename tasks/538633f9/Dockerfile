# Container for the “capacity-planner” encryption task.
# Pre-populates the CSV data file and installs the required tools.

FROM ubuntu:22.04

RUN set -e && \
    apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        gnupg \
        python3 \
        python3-pip && \
    python3 -m pip install --no-cache-dir --upgrade pip && \
    python3 -m pip install --no-cache-dir pytest && \
    mkdir -p /home/user/capacity_tasks && \
    chmod 0777 /home/user && \
    chmod 0777 /home/user/capacity_tasks

RUN cat > /home/user/capacity_tasks/resource_usage.csv << 'EOF'
timestamp,cpu_usage_percent,memory_usage_mb
2024-06-01T00:00:00Z,32,2048
2024-06-01T01:00:00Z,45,3072
2024-06-01T02:00:00Z,29,1984
EOF

RUN chmod 0644 /home/user/capacity_tasks/resource_usage.csv

ENV GPG_TTY=""

RUN chmod 755 /home/user

CMD echo "This container prepares the initial state for the capacity-planner exercise." && \
    echo "Execute your solution inside the container as needed."