# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# Help text
# This image contains the baseline environment for the "capacity-planner" assignment.
# Pre-populated inputs:
#   /home/user/cluster_logs/nodeA.log
#   /home/user/cluster_logs/nodeB.log
#   /home/user/cluster_logs/nodeC.log
# Python (with pytest) is installed so automated grading can run.

LABEL Author="capacity-planning-task"
LABEL Version="v1.0"

ENV PATH=/usr/local/bin:$PATH

RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        ca-certificates && \
    rm -rf /var/lib/apt/lists/*

RUN --mount=type=cache,target=/root/.cache/pip pip3 install --no-cache-dir pytest

RUN mkdir -p /home/user/cluster_logs

RUN cat >/home/user/cluster_logs/nodeA.log <<'EOF'
timestamp,cpu_percent,mem_mb,net_in_mb,net_out_mb
2024-05-01T00:00:00Z,45,1024,50,20
2024-05-01T01:00:00Z,55,1100,60,25
2024-05-01T02:00:00Z,65,1150,70,30
2024-05-01T03:00:00Z,75,1200,80,35
2024-05-01T04:00:00Z,85,1250,90,40
EOF

RUN cat >/home/user/cluster_logs/nodeB.log <<'EOF'
timestamp,cpu_percent,mem_mb,net_in_mb,net_out_mb
2024-05-01T00:00:00Z,35,2048,20,10
2024-05-01T01:00:00Z,40,2100,25,12
2024-05-01T02:00:00Z,60,2200,35,15
2024-05-01T03:00:00Z,70,2300,45,18
2024-05-01T04:00:00Z,95,2400,55,20
EOF

RUN cat >/home/user/cluster_logs/nodeC.log <<'EOF'
timestamp,cpu_percent,mem_mb,net_in_mb,net_out_mb
2024-05-01T00:00:00Z,20,512,10,5
2024-05-01T01:00:00Z,25,520,12,6
2024-05-01T02:00:00Z,30,530,14,7
2024-05-01T03:00:00Z,40,540,16,8
2024-05-01T04:00:00Z,50,550,18,9
EOF

RUN chmod 755 /home/user && \
    chmod 755 /home/user/cluster_logs && \
    chmod 644 /home/user/cluster_logs/*.log