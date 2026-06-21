FROM ubuntu:22.04

# Labels
LABEL Author="task-setup"
LABEL Description="Initial state for the \"alert logs archive & restore\" task with pytest installed."

RUN set -e && \
    export DEBIAN_FRONTEND=noninteractive && \
    apt-get update -y && \
    apt-get install -y python3 python3-pip && \
    pip3 install --no-cache-dir pytest

RUN mkdir -p /home/user/alerts && \
    chmod 0755 /home /home/user /home/user/alerts

RUN printf 'CPU: all good\n' > /home/user/alerts/cpu.log && \
    printf 'MEM: ok\n' > /home/user/alerts/memory.log && \
    printf 'DISK: 70%%\n' > /home/user/alerts/disk.log && \
    chmod 755 /home/user && \
    chmod 0644 /home/user/alerts/*.log