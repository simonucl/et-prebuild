FROM ubuntu:22.04

# Help / labels
LABEL Author="Apptainer Setup Script"
LABEL Description="Container for network-health diagnostics task – provides initial data, pytest, and writable workspace."

# 1. Base system utilities and Python tooling
RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        ca-certificates && \
    rm -rf /var/lib/apt/lists/*

RUN pip3 install --no-cache-dir pytest

# 2. Prepare initial filesystem state for the assignment
RUN mkdir -p /home/user/data/raw
RUN chmod -R 0777 /home/user

# 3. Seed the required raw CSV file
RUN cat > /home/user/data/raw/net_diag_2023-09.csv <<'EOF'
timestamp,source,destination,transmitted,received,packet_loss_percent,min_ms,avg_ms,max_ms,mdev_ms
2023-09-15T10:00:00Z,etl1,db.internal,10,10,0,0.23,0.50,0.75,0.05
2023-09-15T10:05:00Z,etl1,db.internal,10,9,10,0.24,0.55,1.20,0.12
2023-09-15T10:10:00Z,etl1,api.internal,10,10,0,0.30,0.45,0.70,0.07
2023-09-15T10:15:00Z,etl1,api.internal,10,8,20,0.35,0.60,1.10,0.10
EOF

RUN chmod 0644 /home/user/data/raw/net_diag_2023-09.csv

# Environment variables
RUN chmod 755 /home/user
ENV LC_ALL=C.UTF-8
ENV PYTHONUNBUFFERED=1