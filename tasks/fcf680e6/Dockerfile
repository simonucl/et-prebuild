# Author: Performance-Tuning Demo
# Description: Base image with compute.sh and pytest installed for timing task

FROM ubuntu:22.04

ENV PATH=/usr/local/bin:/usr/bin:/bin:$PATH

RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        time \
        ca-certificates && \
    rm -rf /var/lib/apt/lists/*

RUN pip3 install --no-cache-dir pytest

RUN mkdir -p /home/user/app

RUN cat << "EOF" > /home/user/app/compute.sh
#!/bin/bash
# Simple compute-intensive script
sum=0
for i in $(seq 1 100000); do
  sum=$((sum + i))
done
echo $sum
EOF

RUN chmod 0755 /home/user/app/compute.sh

RUN chmod 0755 /home/user