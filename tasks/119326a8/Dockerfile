FROM ubuntu:22.04

# Author: Container-Setup
# Description: Initial state for FinOps cost-report task

RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends python3 python3-pip && \
    pip3 install --no-cache-dir pytest

RUN if ! id -u 1000 >/dev/null 2>&1; then \
        adduser --disabled-password --gecos "" --uid 1000 user; \
    fi

RUN install -o user -g user -d -m 0755 /home/user/bin && \
    install -o user -g user -d -m 0755 /home/user/container_usage

RUN cat >/home/user/container_usage/usage.log <<'EOF'
container_id,image,cpu_percent,mem_mb,runtime_hours,cost_per_hour
a1b2c3,nginx:1.21,15,128,50,0.05
d4e5f6,redis:6,25,256,120,0.03
g7h8i9,postgres:13,55,512,200,0.1
j0k1l2,customapp:latest,65,1024,75,0.2
m3n4o5,python:3.9,10,256,30,0.04
EOF

RUN chown user:user /home/user/container_usage/usage.log && \
    chmod 600 /home/user/container_usage/usage.log

RUN chmod 755 /home/user

ENV PATH="/home/user/bin:${PATH}"

# Container for FinOps cost-report exercise.