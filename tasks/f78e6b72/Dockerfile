FROM ubuntu:22.04

# Help section
# Container for Capacity Planning task. Use apptainer exec/run to work.

RUN set -e && \
    apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest && \
    mkdir -p /home/user && \
    mkdir -p /home/user/capacity && \
    chmod 777 /home/user/capacity

RUN cat > /home/user/capacity/raw_usage.log <<'EOF'
2023-09-01T00:00 serverA 45 70
2023-09-01T01:00 serverB 60 65
2023-09-01T02:00 serverA 55 85
2023-09-01T03:00 serverC N/A 40
2023-09-01T04:00 serverB 75 82
2023-09-01T05:00 serverC 30 90
2023-09-01T06:00 serverA 65 75
2023-09-01T07:00 serverB 50 79
EOF

RUN chmod 644 /home/user/capacity/raw_usage.log && \
    chmod 755 /home/user

ENV PYTHONPATH=/usr/local/lib/python3.10/site-packages:$PYTHONPATH
ENV PATH=/usr/local/bin:$PATH