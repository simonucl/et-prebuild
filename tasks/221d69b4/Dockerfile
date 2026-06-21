FROM ubuntu:22.04

# Help:
# This Apptainer image contains the initial state required for the
# “backup overview” shell task. It pre-installs pytest and provides the
# /home/user/backups/all_backups.csv seed file so that automated tests
# can verify the setup before the student begins working.

# Labels
LABEL Author="dbe-reliability-task"

ENV HOME=/home/user

RUN set -e && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        ca-certificates && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN mkdir -p /home/user/backups && \
    chmod 777 /home/user && \
    chmod 777 /home/user/backups

RUN cat > /home/user/backups/all_backups.csv <<'EOF'
backup_id,db_name,timestamp,size_mb,compressed_size_mb,checksum
bkp-20240101-pg,customerdb,2024-01-01T02:05:00Z,10240,2048,a1b2c3d4
bkp-20240102-mysql,ordersdb,2024-01-02T03:10:00Z,5120,1024,b2c3d4e5
bkp-20240103-pg,inventorydb,2024-01-03T01:55:00Z,20480,4096,c3d4e5f6
bkp-20240104-mysql,analyticsdb,2024-01-04T04:20:00Z,102400,20480,d4e5f6g7
EOF

RUN chmod 666 /home/user/backups/all_backups.csv