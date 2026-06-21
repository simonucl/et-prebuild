FROM ubuntu:22.04

# Help text
# This container provides the initial state for the performance report
# assignment. The critical snapshot file is located at
# /home/user/data/sys_snapshot.log. Pytest is pre-installed so that the
# automated grading harness can run its tests without additional setup.

LABEL Author="performance-engineering-setup"

ENV HOME=/home/user

RUN set -e && \
    apt-get update -qq && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest

RUN mkdir -p /home/user/data && \
    chmod 777 /home/user && \
    chmod 755 /home/user/data

RUN cat <<'EOF' > /home/user/data/sys_snapshot.log
PROC,102,0.3,1.2,bash
PROC,205,25.6,10.1,python3
PROC,309,50.8,5.0,java
PROC,410,12.3,2.1,node
MEM,TotalMemMB,7984
MEM,FreeMemMB,1024
CPU,CoreCount,4
CPU,LoadAvg1min,3.12
DISK,/dev/sda1,UsedPct,65
EOF

RUN chmod 644 /home/user/data/sys_snapshot.log

RUN apt-get clean && rm -rf /var/lib/apt/lists/*