FROM ubuntu:22.04

# Set environment variables
ENV LANG=C
ENV LC_ALL=C

# ---------- System packages ----------
RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        gzip \
        ca-certificates && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# ---------- Python packages ----------
RUN pip3 install --no-cache-dir pytest pandas numpy scipy

# ---------- Dataset preparation ----------
RUN mkdir -p /home/user/data/traffic_logs && \
    chmod 755 /home/user && \
    chmod 755 /home/user/data && \
    chmod 755 /home/user/data/traffic_logs

# ----- region1 -----
RUN cat > /tmp/region1.log <<'EOF'
[2023-05-01 08:15:23] 120
[2023-05-01 09:12:11] 110
[2023-05-02 10:03:42] 140
[2023-05-02 11:33:08] 150
[2023-05-03 08:01:55] 200
EOF

RUN gzip -c /tmp/region1.log > /home/user/data/traffic_logs/region1.log.gz

# ----- region2 -----
RUN cat > /tmp/region2.log <<'EOF'
[2023-05-01 07:55:03] 100
[2023-05-01 12:34:55] 130
[2023-05-02 13:22:11] 160
[2023-05-03 09:45:31] 190
[2023-05-03 19:25:00] 210
EOF

RUN gzip -c /tmp/region2.log > /home/user/data/traffic_logs/region2.log.gz

# ----- region3 -----
RUN cat > /tmp/region3.log <<'EOF'
[2023-05-01 06:45:13] 115
[2023-05-02 14:11:09] 155
[2023-05-02 15:22:05] 165
[2023-05-03 10:33:59] 205
[2023-05-03 11:00:22] 195
EOF

RUN gzip -c /tmp/region3.log > /home/user/data/traffic_logs/region3.log.gz

# Clean up temporary files
RUN rm /tmp/region1.log /tmp/region2.log /tmp/region3.log

# Correct permissions for input files
RUN chmod 644 /home/user/data/traffic_logs/*.log.gz

# Set working directory
WORKDIR /home/user

# Default command
CMD echo "Docker image ready for data-centre latency analysis." && echo "You are now inside the container. Happy hacking!"