FROM ubuntu:22.04

# Environment variables
ENV LANG=C.UTF-8
ENV LC_ALL=C.UTF-8

# Install utilities, Python, and pytest
RUN set -e && \
    apt-get update && \
    apt-get install -y --no-install-recommends python3-pip ca-certificates && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Create directories
RUN mkdir -p /home/user/monitoring/logs

# Create cpu_stats.csv
RUN cat > /home/user/monitoring/logs/cpu_stats.csv <<'EOF'
timestamp,host,cpu_usage,proc_run
2023-08-01T00:00:00Z,web01,25,120
2023-08-01T00:05:00Z,db01,45,87
2023-08-01T00:10:00Z,web01,27,122
2023-08-01T00:15:00Z,db01,46,90
EOF

# Create mem_stats.csv
RUN cat > /home/user/monitoring/logs/mem_stats.csv <<'EOF'
timestamp,host,mem_free,swap_used
2023-08-01T00:00:00Z,web01,1024,128
2023-08-01T00:05:00Z,db01,512,256
2023-08-01T00:10:00Z,web01,1000,130
2023-08-01T00:15:00Z,db01,500,260
EOF

# Permissions adjustments
RUN chmod 644 /home/user/monitoring/logs/*.csv && \
    chmod 777 /home/user/monitoring && \
    chmod 755 /home && \
    chmod 755 /home/user

# Default runscript behavior
CMD ["/bin/bash"]