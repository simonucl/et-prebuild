FROM ubuntu:22.04

# help:
# This container image sets up the initial filesystem state for the
# “Disk Reports” exercise. It installs pytest for automated grading and
# creates the three source CSV files required by the assignment.

LABEL Author="disk-report-initializer"

ENV HOME=/home/user

RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends python3 python3-pip && \
    pip3 install --no-cache-dir pytest && \
    mkdir -p /home/user/disk_reports

RUN cat > /home/user/disk_reports/server_a.csv << 'EOF'
mount_point,total_gb,used_gb
/,50,30
/home,200,150
/var,100,90
EOF

RUN cat > /home/user/disk_reports/server_b.csv << 'EOF'
mount_point,total_gb,used_gb
/,60,20
/home,250,240
/opt,80,30
EOF

RUN cat > /home/user/disk_reports/server_c.csv << 'EOF'
mount_point,total_gb,used_gb
/,40,35
/data,500,450
/backup,300,100
EOF

RUN chmod 755 /home/user && \
    chmod 755 /home/user/disk_reports && \
    chmod 644 /home/user/disk_reports/server_*.csv