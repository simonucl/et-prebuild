FROM ubuntu:22.04

# Install Python tooling and pytest
RUN set -e && \
    apt-get update -qq && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y -qq python3-pip --no-install-recommends && \
    pip3 install --no-cache-dir pytest

# Create directory structure
RUN mkdir -p /home/user/metrics/raw && \
    mkdir -p /home/user/grafana/dashboards

# Populate raw latency log files
RUN cat > /home/user/metrics/raw/serviceA-2023-10-01.log <<'EOF'
2023-10-01T00:00:01Z serviceA 120 200
2023-10-01T00:00:02Z serviceA 250 200
2023-10-01T00:00:03Z serviceA 110 500
EOF

RUN cat > /home/user/metrics/raw/serviceB-2023-10-01.log <<'EOF'
2023-10-01T00:00:01Z serviceB 95 200
2023-10-01T00:00:02Z serviceB 105 200
EOF

# Create Grafana dashboard template
RUN cat > /home/user/grafana/dashboards/sample_dashboard.conf <<'EOF'
cpu_threshold=PLACEHOLDER_CPU_THRESHOLD
mem_threshold=PLACEHOLDER_MEM_THRESHOLD
disk_threshold=PLACEHOLDER_DISK_THRESHOLD
EOF

# Set liberal permissions
RUN chmod -R 0777 /home/user

# Labels
LABEL Author="Apptainer Task Preparer"
LABEL Description="Environment for observability shell-task with pytest installed"

# Environment variables
ENV PATH=/usr/local/bin:/usr/bin:/bin:$PATH

CMD ["bash"]