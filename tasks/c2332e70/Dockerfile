# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# Help / metadata
LABEL Author="Bulk-compress exercise bootstrap"
LABEL Description="Environment with initial ticket logs for compression task."

ENV LC_ALL=C.UTF-8
ENV PATH=/usr/local/bin:/usr/bin:/bin:$PATH

RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip set -e && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
        python3-pip \
        python3-setuptools \
        python3-wheel \
        findutils \
        gzip && \
    pip3 install --no-cache-dir pytest && \
    mkdir -p /home/user/support-logs && \
    chmod 777 /home/user/support-logs && \
    printf 'System rebooted OK\n' > /home/user/support-logs/ticket_123.log && \
    printf 'Disk cleanup completed' > /home/user/support-logs/ticket_124.log && \
    printf 'VPN credentials reset' > /home/user/support-logs/ticket_125.log && \
    echo 'These are daily support logs. Compress old ones regularly.' > /home/user/support-logs/README.txt && \
    chmod 644 /home/user/support-logs/ticket_123.log \
              /home/user/support-logs/ticket_124.log \
              /home/user/support-logs/ticket_125.log \
              /home/user/support-logs/README.txt && \
    rm -rf /var/lib/apt/lists/*

RUN chmod 755 /home/user