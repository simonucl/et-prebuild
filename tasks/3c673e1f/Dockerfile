FROM ubuntu:22.04

# Author observability-benchmark
# Description Base image for latency-panel micro-benchmark task

RUN apt-get update && \
    apt-get install -y --no-install-recommends python3 python3-pip && \
    pip3 install --no-cache-dir pytest && \
    mkdir -p /home/user && \
    chmod 755 /home/user && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

ENV PATH=/usr/local/bin:/usr/bin:/bin

CMD /bin/sh -c "echo 'Container for latency-panel micro-benchmark task.' && echo 'Run your benchmark script inside this container.'"