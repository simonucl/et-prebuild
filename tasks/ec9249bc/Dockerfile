# This image provides the initial filesystem and dependencies
# for the latency log summarization task.
# Directories and log files are pre-seeded in /home/user/services/.
# pytest is installed for automated grading.

FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && \
    apt-get install -y --no-install-recommends python3 python3-pip && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

RUN mkdir -p /home/user/services/auth/logs && \
    mkdir -p /home/user/services/inventory/logs

RUN cat << 'EOF' > /home/user/services/auth/logs/request.log
1609459201000 15
1609459202000 10
1609459203000 20
1609459204000 5
1609459205000 15
EOF

RUN cat << 'EOF' > /home/user/services/inventory/logs/request.log
1609459201100 30
1609459202100 25
1609459203100 35
1609459204100 40
EOF

RUN chmod -R 777 /home/user