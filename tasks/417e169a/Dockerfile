FROM ubuntu:22.04

# Install Python and pytest
RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest

# Prepare initial diagnostics data
RUN mkdir -p /home/user/diagnostics

RUN cat > /home/user/diagnostics/cpu_dump.txt <<'EOF'
Model name: Intel(R) Xeon(R) CPU E5-2630 v4 @ 2.20GHz
CPU(s): 16
Thread(s) per core: 2
EOF

RUN cat > /home/user/diagnostics/mem_dump.txt <<'EOF'
MemTotal: 32000 MB
MemFree: 12000 MB
MemAvailable: 15000 MB
EOF

RUN cat > /home/user/diagnostics/disk_dump.txt <<'EOF'
DiskSize: 500 GB
DiskUsed: 123 GB
DiskAvailable: 377 GB
EOF

# Set permissions
RUN chmod 755 /home/user && \
    chmod 755 /home/user/diagnostics && \
    chmod 644 /home/user/diagnostics/*.txt

# Environment variables
ENV PATH=/usr/local/bin:/usr/bin:/bin:$PATH

# Runscript equivalent
CMD echo "Container for diagnostics snapshot task is ready."