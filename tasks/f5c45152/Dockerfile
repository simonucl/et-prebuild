FROM ubuntu:22.04

# Author network-task-prep
# Description "Environment prepared for the network normalisation task"

RUN set -eux && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        sqlite3 \
        ca-certificates && \
    python3 -m pip install --no-cache-dir --upgrade pip && \
    python3 -m pip install --no-cache-dir pytest && \
    mkdir -p /home/user/network_diag && \
    chmod 777 /home/user/network_diag && \
    mkdir -p /home/user && \
    chmod 777 /home/user

RUN cat > /home/user/network_diag/devices.csv <<'EOF'
id,hostname,mgmt_ip,site
1,edge-rt1,192.0.2.1,NYC
2,core-sw1,192.0.2.2,NYC
3,dist-sw1,192.0.2.3,SFO
4,edge-rt2,192.0.2.4,SFO
5,branch-rt1,192.0.2.5,LON
EOF

RUN cat > /home/user/network_diag/pings.csv <<'EOF'
id,device_id,rtt_ms,success,ts_utc
1,1,4.22,1,2023-12-01T12:00:00Z
2,1,4.10,1,2023-12-01T12:05:00Z
3,1,,0,2023-12-01T12:10:00Z
4,2,0.80,1,2023-12-01T12:00:00Z
5,2,0.75,1,2023-12-01T12:05:00Z
6,3,20.21,1,2023-12-01T12:00:00Z
7,3,,0,2023-12-01T12:05:00Z
8,3,,0,2023-12-01T12:10:00Z
9,4,18.40,1,2023-12-01T12:00:00Z
10,4,18.10,1,2023-12-01T12:05:00Z
11,5,90.50,1,2023-12-01T12:00:00Z
12,5,,0,2023-12-01T12:05:00Z
EOF

RUN chmod 666 /home/user/network_diag/devices.csv /home/user/network_diag/pings.csv && \
    chmod 755 /home/user

ENV PATH="/usr/local/bin:/usr/bin:/bin:$PATH"

# This container is prepared for the network normalisation task.
# Invoke your own commands within the container or use an interactive shell.