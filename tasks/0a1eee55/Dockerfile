FROM ubuntu:22.04

# Install required packages and pytest
RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
    && rm -rf /var/lib/apt/lists/*

RUN pip3 install --no-cache-dir pytest

# Create directory structure
RUN mkdir -p /home/user/data

# CPU metrics
RUN cat > /home/user/data/resource_cpu.csv <<'EOF'
timestamp,hostname,cpu_percent
2023-07-01T00:00:00Z,web-1,55
2023-07-01T01:00:00Z,web-1,60
2023-07-01T00:00:00Z,db-1,75
2023-07-01T01:00:00Z,db-1,70
2023-07-01T00:00:00Z,worker-1,30
2023-07-01T01:00:00Z,worker-1,40
EOF

# Memory metrics
RUN cat > /home/user/data/resource_memory.csv <<'EOF'
timestamp,hostname,mem_mb
2023-07-01T00:00:00Z,web-1,2048
2023-07-01T01:00:00Z,web-1,2100
2023-07-01T00:00:00Z,db-1,4096
2023-07-01T01:00:00Z,db-1,4200
2023-07-01T00:00:00Z,worker-1,1024
2023-07-01T01:00:00Z,worker-1,1100
EOF

# Disk metrics
RUN cat > /home/user/data/resource_disk.csv <<'EOF'
timestamp,hostname,disk_gb
2023-07-01T00:00:00Z,web-1,120
2023-07-01T01:00:00Z,web-1,121
2023-07-01T00:00:00Z,db-1,300
2023-07-01T01:00:00Z,db-1,302
2023-07-01T00:00:00Z,worker-1,80
2023-07-01T01:00:00Z,worker-1,81
EOF

# Permissions
RUN chmod 0644 /home/user/data/resource_*.csv && \
    chmod 0755 /home/user /home/user/data

# Environment
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

RUN chmod 755 /home/user

# Labels
LABEL Author="OpenAI ChatGPT"
LABEL Description="Container providing initial state for capacity-planning analyst task (includes test data and pytest)."