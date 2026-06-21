FROM ubuntu:22.04

# Help / labels
LABEL Author="Apptainer Task Generator"
LABEL Description="Environment with preset logs and cache directories for disk-usage observability exercise."

# Environment variables
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

# Post section
RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        ca-certificates \
        coreutils && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN pip3 install --no-cache-dir pytest

RUN mkdir -p /home/user && \
    mkdir -p /home/user/app_logs && \
    truncate -s 123  /home/user/app_logs/api.log && \
    truncate -s 2048 /home/user/app_logs/db.log && \
    mkdir -p /home/user/cache && \
    truncate -s 4096 /home/user/cache/temp1.bin && \
    truncate -s 1024 /home/user/cache/temp2.bin && \
    chmod 0755 /home/user && \
    chmod 0755 /home/user/app_logs && \
    chmod 0755 /home/user/cache && \
    chmod 0644 /home/user/app_logs/api.log && \
    chmod 0644 /home/user/app_logs/db.log && \
    chmod 0644 /home/user/cache/temp1.bin && \
    chmod 0644 /home/user/cache/temp2.bin && \
    rm -rf /home/user/obs_metrics || true

# Ensure permissions at runtime (from %environment section)
RUN chmod 755 /home/user

CMD echo "Container for observability disk-usage task." && echo "Nothing to run by default."